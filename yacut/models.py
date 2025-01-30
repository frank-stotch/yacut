from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .settings import (
    MAX_GENERATE_SHORT_RETRIES,
    MAX_SHORT_LENGTH,
    POSSIBLE_CHARACTERS,
    RANDOM_SHORT_LENGTH,
    REDIRECT_VIEW
)


ORIGINAL_MAX_LENGTH = 256


class Message:
    SHORT_ALREADY_EXISTS = 'Вариант короткой ссылки "{}" уже существует'
    REQUIRED_FIELD = 'Обязательное поле'
    INVALID_URL_PATTERN = 'Неправильный формат ссылки'
    INVALID_SHORT_ID_PATTERN = ('Можно использовать только'
                                ' латинские буквы и цифры')
    INVALID_SHORT_ID_LENGTH = ('Длина короткой ссылки '
                               f'до {MAX_SHORT_LENGTH}')
    FILTERS_REQUIRED = 'Нужно передать хотя бы один фильтр'
    INVALID_FILTERS = 'Некорректные поля {}'


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
    def create(original, short):
        db.session.add(URLMap(original=original, short=short))
        db.session.commit()

    @staticmethod
    def from_short(short):
        entry = URLMap.query.filter_by(short=short).first()
        if entry:
            return entry.original

    @staticmethod
    def generate_short():
        retry = 1
        while retry <= MAX_GENERATE_SHORT_RETRIES:
            short = ''.join(
                choices(POSSIBLE_CHARACTERS, k=RANDOM_SHORT_LENGTH)
            )
            if not URLMap.query.filter_by(short=short).first():
                return short
            retry += 1

    @staticmethod
    def get_url_for_short(short):
        entry = URLMap.query.filter_by(short=short).first()
        if entry:
            return url_for(REDIRECT_VIEW, short=short, _external=True)
