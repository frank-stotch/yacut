import os


SHORT_ID_PATTERN = r'[A-Za-z0-9]+'
SHORT_ID_LENGTH = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'MUMBAYUMBA')
