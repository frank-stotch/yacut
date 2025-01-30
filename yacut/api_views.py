from http import HTTPStatus
import re
from urllib.parse import urlparse

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import SHORT_ID_LENGTH, SHORT_ID_PATTERN
from .views import get_unique_short_id


ENTRY_DOES_NOT_EXIST = 'Указанный id не найден'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
REQUIRED_FIELD_MISSING = '"{}" является обязательным полем!'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL = 'Недопустимый формат url'
SHORT_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
URL_FIELD_NAME = 'url'
CUSTOM_ID_FIELD_NAME = 'custom_id'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    entry = URLMap.query.filter_by(short=short_id).first()
    if not entry:
        raise InvalidAPIUsage(ENTRY_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND)
    return jsonify({'url': entry.original}), HTTPStatus.OK


def get_original(original_field_name: str, data: dict):
    original = data.get(original_field_name)
    if not original:
        raise InvalidAPIUsage(
            REQUIRED_FIELD_MISSING.format(original_field_name))
    parsed = urlparse(original)
    if not all([parsed.scheme, parsed.netloc]):
        raise InvalidAPIUsage(INVALID_ORIGINAL)
    return original


def get_short(short_field_name: str, data: dict):
    short = data.get(short_field_name)
    if not short:
        return get_unique_short_id()
    if (
        len(short) > SHORT_ID_LENGTH
        or not re.fullmatch(SHORT_ID_PATTERN, short)
    ):
        raise InvalidAPIUsage(INVALID_SHORT)
    if URLMap.exists(short=short):
        raise InvalidAPIUsage(SHORT_ALREADY_EXISTS)
    return short


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    short = get_short(CUSTOM_ID_FIELD_NAME, data)
    original = get_original(URL_FIELD_NAME, data)
    entry = URLMap(original=original, short=short)
    entry.save()
    return jsonify(
        {
            'url': original,
            'short_link':
            url_for('redirect_view', short_id=short, _external=True)
        }
    ), HTTPStatus.CREATED