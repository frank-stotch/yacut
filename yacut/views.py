from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.build_short_url(
                URLMap.create(original=form.original_link.data,
                              short=form.custom_id.data,
                              full_validation=False
                              ).short
            )
        )
    except (ValueError, RuntimeError) as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short: str):
    entry = URLMap.get(short=short)
    if not entry:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(entry.original)
