import os

URL_POSTFIX_SIZE = 6
DOMAIN_PREFIX_LIST = ['yacut.ru/', 'http://yacut.ru/', 'https://yacut.ru/']

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
