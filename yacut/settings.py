import os
from string import ascii_letters, digits


POSSIBLE_CHARACTERS = ascii_letters + digits
SHORT_PATTERN = rf'^[{POSSIBLE_CHARACTERS}]+'
MAX_SHORT_LENGTH = 16

RANDOM_SHORT_LENGTH = 6
MAX_GENERATE_SHORT_RETRIES = 10

REDIRECT_VIEW = 'redirect_view'


ORIGINAL_MAX_LENGTH = 2000


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'MUMBAYUMBA')
