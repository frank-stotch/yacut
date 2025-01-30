from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .models import Message, ORIGINAL_MAX_LENGTH
from .settings import MAX_SHORT_LENGTH, SHORT_PATTERN


class Label:
    LONG_URL = 'Длинная ссылка'
    CUSTOM_SHORT_ID = 'Ваш вариант короткой ссылки'
    SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        label=Label.LONG_URL,
        validators=[
            DataRequired(Message.REQUIRED_FIELD),
            URL(message=Message.INVALID_URL_PATTERN),
            Length(max=ORIGINAL_MAX_LENGTH,
                   message=Message.INVALID_ORIGINAL_LENGTH)
        ]
    )
    custom_id = StringField(
        label=Label.CUSTOM_SHORT_ID,
        validators=[
            Optional(),
            Regexp(SHORT_PATTERN, message=Message.INVALID_SHORT_PATTERN),
            Length(max=MAX_SHORT_LENGTH,
                   message=Message.INVALID_SHORT_LENGTH)
        ]
    )
    submit = SubmitField(label=Label.SUBMIT)
