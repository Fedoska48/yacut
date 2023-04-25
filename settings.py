import os

# settings

DOMAIN = 'http://localhost/'


# messages

# serizalization
API_FIELDS = {
    'url': 'original',
    'custom_id': 'short',
}


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
