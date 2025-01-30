from werkzeug.routing import BaseConverter


class ShortIDConverter(BaseConverter):
    regex = r'^[a-zA-Z0-9]{1,16}$'
