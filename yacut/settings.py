import os
from string import ascii_letters, digits


SHORT_ID_PATTERN = r'[A-Za-z0-9]+'
SHORT_ID_LENGTH = 16
RANDOM_SHORT_ID_LENGTH = 6
POSSIBLE_CHARACTERS = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'MUMBAYUMBA')
