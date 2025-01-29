from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ENTRY_DOES_NOT_EXIST = "Указанный id не найден"


@app.route('/api/id/<str:short_id>')
def get_url(short_id):
    entry = URLMap.query.filter_by(short=short_id).first()
    if not entry:
        raise InvalidAPIUsage(ENTRY_DOES_NOT_EXIST)
    return (
        jsonify(
            {'url':
             url_for('redirect_view', short_id=entry.short, _external=True)}
        ),
        HTTPStatus.OK
    )