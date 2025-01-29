from random import choices
from string import ascii_letters, digits

from flask import flash, redirect, render_template, url_for
from werkzeug.exceptions import BadRequest

from . import app
from .forms import URLMapForm
from .models import Message, MaxLength, URLMap


POSSIBLE_CHARACTERS = ascii_letters + digits
SHORT_ID_READY = ('Ваша короткая ссылка готова: '
                  '<a href="{short}">{short}</a>')
SHORT_ALREADY_EXISTS = ('Вариант короткой ссылки '
                        '<a href="{short}">{short}</a> уже существует')


def get_unique_short_id():
    """
    Генерирует уникальный короткий ID, который не существует в базе данных.
    """
    while True:
        short_id = ''.join(choices(POSSIBLE_CHARACTERS,
                           k=MaxLength.RANDOM_SHORT_ID))
        if not URLMap.exists(short=short_id):
            return short_id


def get_unique_short_id_or_400(custom_short_id=None):
    if custom_short_id:
        if URLMap.exists(short=custom_short_id):
            short_url = url_for(
                'redirect_view', short_id=custom_short_id, _external=True)
            raise BadRequest(SHORT_ALREADY_EXISTS.format(short=short_url))
        return custom_short_id
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short_id = get_unique_short_id_or_400(form.custom_id.data)
        entry = URLMap(original=original, short=short_id)
        entry.save()
        short_url = url_for('redirect_view', short_id=short_id, _external=True)
        flash(SHORT_ID_READY.format(short=short_url), 'success')
    return render_template('index.html', form=form)


@app.route('/<short_id:short_id>')
def redirect_view(short_id):
    entry = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(entry.original)
