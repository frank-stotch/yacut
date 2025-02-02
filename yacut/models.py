import re
from datetime import datetime
from random import choices
from typing import Union

from flask import url_for

from . import db
from .settings import (
    MAX_GENERATE_SHORT_RETRIES,
    MAX_SHORT_LENGTH,
    ORIGINAL_MAX_LENGTH,
    POSSIBLE_CHARACTERS,
    RANDOM_SHORT_LENGTH,
    REDIRECT_VIEW,
    SHORT_PATTERN
)

GENERATION_FAILED = ('Не получилось сгенерировать короткую ссылку. '
                     f'за {MAX_GENERATE_SHORT_RETRIES} попыток. '
                     'Попробуйте ещё раз.')
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL = 'Недопустимый формат url'
SHORT_ALREADY_EXISTS = ('Предложенный вариант короткой ссылки '
                        'уже существует.')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH),
                      nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow)

    @staticmethod
    def create(
        original: str,
        short: Union[str, None] = None,
        full_validation=True
    ):
        if short:
            if full_validation:
                if len(short) > MAX_SHORT_LENGTH:
                    raise ValueError(INVALID_SHORT)
                if not re.fullmatch(SHORT_PATTERN, short):
                    raise ValueError(INVALID_SHORT)
            if URLMap.get(short):
                raise ValueError(SHORT_ALREADY_EXISTS)
        else:
            short = URLMap.generate_short()
        if full_validation and len(original) > ORIGINAL_MAX_LENGTH:
            raise ValueError(INVALID_ORIGINAL)
        entry = URLMap(original=original, short=short)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get(short: str):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short():
        for _ in range(MAX_GENERATE_SHORT_RETRIES):
            short = ''.join(
                choices(POSSIBLE_CHARACTERS, k=RANDOM_SHORT_LENGTH)
            )
            if not URLMap.get(short):
                return short
        raise RuntimeError(GENERATION_FAILED)

    @staticmethod
    def build_short_url(short: str):
        return url_for(REDIRECT_VIEW, short=short, _external=True)
