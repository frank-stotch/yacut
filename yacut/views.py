from http import HTTPStatus
from random import choices
from string import ascii_letters, digits

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import URLMapForm
from .models import Message, MaxLength, URLMap


POSSIBLE_CHARACTERS = ascii_letters + digits


def get_unique_short_id():
    while True:
        short_id = ''.join(choices(POSSIBLE_CHARACTERS,
                                   k=MaxLength.RANDOM_SHORT_ID))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id