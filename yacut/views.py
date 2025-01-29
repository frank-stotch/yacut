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


def get_unique_short_id():
    """
    Генерирует уникальный короткий ID, который не существует в базе данных.
    """
    while True:
        short_id = ''.join(choices(POSSIBLE_CHARACTERS,
                           k=MaxLength.RANDOM_SHORT_ID))
        if not URLMap.exists(short=short_id):
            return short_id


def create_or_get_short_url(original, custom_short_id=None):
    """
    Если пользователь передал  custom_short_id, то проверяет наличие в БД.
    При его наличии в БД, бросает исключение. Если custom_short_id новый,
    то возвращает это его и True (можно создать запись в БД).

    Если свой short_id не передан, то проверяет наличие original ссылки в БД.
    Если она есть, то возвращает имеющийся short
    и False (создать запись нельзя). В противном случае генерирует
    custom_short_id, возвращает его и True (можно создать запись в БД)
    """
    if custom_short_id:
        if URLMap.exists(short=custom_short_id):
            raise BadRequest(
                Message.SHORT_ALREADY_EXISTS.format(custom_short_id))
        return custom_short_id, True
    existing_entry = URLMap.query.filter_by(original=original).first()
    if existing_entry:
        return existing_entry.short, False
    return get_unique_short_id(), True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short_id, can_create = create_or_get_short_url(
            original, form.custom_id.data)
        if can_create:
            entry = URLMap(original=original, short=short_id)
            entry.save()
        short_url = url_for('redirect_view', short_id=short_id, _external=True)
        flash(SHORT_ID_READY.format(short_url))
    return render_template('index.html', form=form)


@app.route('/<short_id:short_id>')
def redirect_view(short_id):
    entry = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(entry.original)
