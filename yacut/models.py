import re
from datetime import datetime
from random import choices
from typing import Union
from urllib.parse import urlparse

from flask import url_for

from . import db
from .settings import (
    MAX_GENERATE_SHORT_RETRIES,
    MAX_SHORT_LENGTH,
    POSSIBLE_CHARACTERS,
    RANDOM_SHORT_LENGTH,
    REDIRECT_VIEW,
    SHORT_PATTERN
)


ORIGINAL_MAX_LENGTH = 256


class Message:
    REQUIRED_FIELD = 'Обязательное поле'
    INVALID_URL_PATTERN = 'Неправильный формат ссылки'
    INVALID_SHORT_PATTERN = ('Можно использовать только'
                             ' латинские буквы и цифры')
    INVALID_SHORT_LENGTH = ('Длина короткой ссылки '
                            f'до {MAX_SHORT_LENGTH}')
    INVALID_ORIGINAL_LENGTH = (f'Не более {ORIGINAL_MAX_LENGTH} '
                               'символов в ссылке.')
    GENERATION_FAILED = ('Не получилось сгенерировать короткую ссылку. '
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

    def to_dict(self):
        return {'url': self.original, 'custom_id': self.short}

    @staticmethod
    def create(original: str, short: Union[str, None] = None):
        short = URLMap.get_or_generate_short(short)
        parsed = urlparse(original)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError(Message.INVALID_ORIGINAL)
        entry = URLMap(original=original, short=short)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def from_short(short: str) -> Union[str, None]:
        entry = URLMap.query.filter_by(short=short).first()
        if entry:
            return entry.original

    @staticmethod
    def get_or_generate_short(short: Union[str, None] = None):
        if short:
            if (
                len(short) > MAX_SHORT_LENGTH
                or not re.fullmatch(SHORT_PATTERN, short)
            ):
                raise ValueError(Message.INVALID_SHORT)
            if not URLMap.query.filter_by(short=short).first():
                return short
            raise ValueError(Message.SHORT_ALREADY_EXISTS.format(short))
        for _ in range(MAX_GENERATE_SHORT_RETRIES):
            short = ''.join(
                choices(POSSIBLE_CHARACTERS, k=RANDOM_SHORT_LENGTH)
            )
            if not URLMap.query.filter_by(short=short).first():
                return short
        raise RuntimeError(Message.GENERATION_FAILED)

    @staticmethod
    def get_url_for_short(short: str) -> Union[str, None]:
        entry = URLMap.query.filter_by(short=short).first()
        if entry:
            return url_for(REDIRECT_VIEW, short=short, _external=True)
