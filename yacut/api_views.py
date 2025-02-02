from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import REDIRECT_VIEW


ID_DOES_NOT_EXIST = 'Указанный id не найден'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
ORIGINAL_MISSING = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    entry = URLMap.get(short)
    if not entry:
        raise InvalidAPIUsage(ID_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND)
    return jsonify({'url': entry.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ORIGINAL_MISSING)
    try:
        return jsonify(
            {'url': data['url'],
             'short_link': URLMap.build_short_url(
                 URLMap.create(data['url'],
                               data.get('custom_id')).short)}
        ), HTTPStatus.CREATED
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
