from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .models import Message, MinLength
from .settings import SHORT_ID_LENGTH, SHORT_ID_PATTERN


class Label:
    LONG_URL = 'Длинная ссылка'
    CUSTOM_SHORT_ID = 'Ваш вариант короткой ссылки'
    SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        label=Label.LONG_URL,
        validators=[
            DataRequired(Message.REQUIRED_FIELD),
            URL(message=Message.INVALID_URL_PATTERN)
        ]
    )
    custom_id = StringField(
        label=Label.CUSTOM_SHORT_ID,
        validators=[
            Optional(),
            Regexp(SHORT_ID_PATTERN, message=Message.INVALID_SHORT_ID_PATTERN),
            Length(MinLength.SHORT_ID, SHORT_ID_LENGTH,
                   Message.INVALID_SHORT_ID_LENGTH)
        ]
    )
    submit = SubmitField(label=Label.SUBMIT)
