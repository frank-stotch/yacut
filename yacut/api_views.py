from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ENTRY_DOES_NOT_EXIST = 'Указанный id не найден'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
ORIGINAL_MISSING = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    original = URLMap.from_short(short)
    if not original:
        raise InvalidAPIUsage(ENTRY_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND)
    return jsonify({'url': original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    original = data.get('url')
    if not original:
        raise InvalidAPIUsage(ORIGINAL_MISSING)
    try:
        entry = URLMap.create(original, data.get('custom_id'))
        return jsonify(
            {
                'url': entry.original,
                'short_link': URLMap.get_url_for_short(entry.short)
            }
        ), HTTPStatus.CREATED
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
