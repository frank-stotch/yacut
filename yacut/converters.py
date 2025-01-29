from werkzeug.routing import BaseConverter
from .settings import SHORT_ID_PATTERN


class ShortIDConverter(BaseConverter):
    regex = SHORT_ID_PATTERN
