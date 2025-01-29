from http import HTTPStatus

from flask import flash, jsonify, render_template
from werkzeug.exceptions import BadRequest

from . import app, db
from .forms import URLMapForm


class InvalidAPIUsage(Exception):

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str,
                 status_code=None) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(BadRequest)
def invalid_form_data(error):
    db.session.rollback()
    form = URLMapForm()
    flash(error.description)
    return render_template('index.html', form=form), error.code


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND
