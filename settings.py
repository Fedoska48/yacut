import os

# settings
URL_POSTFIX_SIZE = 6
DOMAIN = 'http://localhost/'
PATTERN = r'^[a-zA-Z0-9]{1,16}$'

# messages
NO_DATA = 'Отсутствует тело запроса'
ALREADY_EXISTS_API = 'Имя "{}" уже занято.'
ALREADY_EXISTS_MAIN = 'Имя {} уже занято!'
PATTERN_ERROR = 'Указано недопустимое имя для короткой ссылки'
REQUIRED_URL_FIELD = '"url" является обязательным полем!'
SHORT_ID_NOT_EXISTS = 'Указанный id не найден'

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
