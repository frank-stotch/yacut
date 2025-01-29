from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .converters import ShortIDConverter
from .settings import Config

app = Flask(__name__)
app.config.from_object(Config)

app.url_map.converters['short_id'] = ShortIDConverter

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, models, views
