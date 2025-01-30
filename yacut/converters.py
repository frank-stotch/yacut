from werkzeug.routing import BaseConverter

from .settings import SHORT_ID_LENGTH


class ShortIDConverter(BaseConverter):
    regex = rf'^[a-zA-Z0-9]{{1,{SHORT_ID_LENGTH}}}$'

