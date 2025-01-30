from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


SHORT_ID_READY = ('Ваша короткая ссылка готова:')


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    try:
        entry = URLMap.create(original=form.original_link.data,
                              short=short)
        return render_template('index.html',
                               form=form,
                               short=URLMap.get_url_for_short(entry.short))
    except ValueError as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short: str):
    original = URLMap.from_short(short=short)
    if not original:
        abort(HTTPStatus.NOT_FOUND)
    redirect(original)
