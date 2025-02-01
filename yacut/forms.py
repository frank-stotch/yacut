from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


from .settings import (
    MAX_SHORT_LENGTH,
    ORIGINAL_MAX_LENGTH,
    SHORT_PATTERN
)


REQUIRED_FIELD = 'Обязательное поле'
INVALID_URL_PATTERN = 'Неправильный формат ссылки'
INVALID_SHORT_PATTERN = ('Можно использовать только'
                         ' латинские буквы и цифры')
INVALID_SHORT_LENGTH = ('Длина короткой ссылки '
                        f'до {MAX_SHORT_LENGTH}')
INVALID_ORIGINAL_LENGTH = (f'Не более {ORIGINAL_MAX_LENGTH} '
                           'символов в ссылке.')

LONG_URL = 'Длинная ссылка'
CUSTOM_SHORT_ID = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        label=LONG_URL,
        validators=[
            DataRequired(REQUIRED_FIELD),
            URL(message=INVALID_URL_PATTERN),
            Length(max=ORIGINAL_MAX_LENGTH,
                   message=INVALID_ORIGINAL_LENGTH)
        ]
    )
    custom_id = StringField(
        label=CUSTOM_SHORT_ID,
        validators=[
            Optional(),
            Regexp(SHORT_PATTERN, message=INVALID_SHORT_PATTERN),
            Length(max=MAX_SHORT_LENGTH,
                   message=INVALID_SHORT_LENGTH)
        ]
    )
    submit = SubmitField(label=SUBMIT)
