import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from sqlalchemy import exists
from sqlalchemy.orm import validates

from . import db
from .settings import SHORT_ID_PATTERN


class MaxLength:
    ORIGINAL_URL = 256
    SHORT_ID = 64


class MinLength:
    ORIGINAL_URL = 3
    SHORT_ID = 1


class Message:
    SHORT_ALREADY_EXISTS = 'Вариант короткой ссылки "{}" уже существует'
    REQUIRED_FIELD = 'Обязательное поле'
    INVALID_URL_PATTERN = 'Неправильный формат ссылки'
    INVALID_SHORT_ID_PATTERN = ('Можно использовать только'
                                ' латинские буквы и цифры')
    INVALID_SHORT_ID_LENGTH = ('Длина короткой ссылки '
                               f'от {MinLength.SHORT_ID} '
                               f'до {MaxLength.SHORT_ID}')
    FILTERS_REQUIRED = 'Нужно передать хотя бы один фильтр'
    INVALID_FILTERS = 'Некорректные поля {}'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MaxLength.ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(MaxLength.SHORT_ID),
                      nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now(timezone.utc))

    @classmethod
    def get_required_fields_names(cls):
        return [
            column.name for column in cls.__table__.columns
            if not column.primary_key
            and not column.default
            and not column.server_default
            and not column.nullable
        ]

    @classmethod
    def get_all_fields_names(cls):
        return [column.name for column in cls.__table__.columns]

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            field_name: getattr(self, field_name)
            for field_name in self.get_all_fields_names()
        }

    def from_dict(self, data: dict):
        for field in self.get_required_fields_names():
            if field in data:
                setattr(self, field, data[field])

    @classmethod
    def __check_filters(cls, **filters):
        if not filters:
            raise ValueError(Message.FILTERS_REQUIRED)
        invalid_keys = set(filters) - set(cls.get_all_fields_names())
        if invalid_keys:
            raise ValueError(Message.INVALID_FILTERS.format(invalid_keys))

    @classmethod
    def exists(cls, **filters):
        cls.__check_filters(**filters)
        return bool(
            db.session.query(
                exists().where(
                    *[getattr(cls, key) == value
                      for key, value in filters.items()]
                )
            ).scalar()
        )

    @validates('original')
    def validate_original(self, key, original: str):
        parsed = urlparse(original)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError(Message.INVALID_URL_PATTERN)
        return original

    @validates('short')
    def validate_short(self, key, short: str):
        if not re.fullmatch(SHORT_ID_PATTERN, short):
            raise ValueError(Message.INVALID_SHORT_ID_PATTERN)
        return short
