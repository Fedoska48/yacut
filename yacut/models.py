import random
import string
from datetime import datetime
from re import fullmatch

from flask import url_for

from yacut import db

# letters, digits
PATTERN = r'^[a-zA-Z0-9]{1,16}$'
LETTERS_AND_DIGITS = string.ascii_letters + string.digits
URL_POSTFIX_SIZE = 6
SHORT_MAX_LEN = 16
ORIGINAL_MAX_LEN = 512

# messages
PATTERN_ERROR = 'Указано недопустимое имя для короткой ссылки'
ORIGINAL_LEN_ERROR = ('Длинна входной ссылки должна быть менее {} символов.'
                      'Ваш  размер: {}')
SHORT_LEN_ERROR = ('Вариант короткой ссылки должен быть не больше {} символов.'
                   'Ваш  размер: {}')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(ORIGINAL_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LEN), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразование объекта модели в словарь (слов
        арь -> JSON)."""
        return dict(
            url=self.original,
            short_link=url_for(
                'url_routing', short=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        """Преобразование словаря в объект модели (JSON -> словарь).
        В пустой объект класса URLMap добавляются поля полученные в POST."""
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def get_unique_short_id():
        """Генератор шестизначного постфикса для ссылки."""
        short_url_postfix = ''.join(
            random.sample(LETTERS_AND_DIGITS, URL_POSTFIX_SIZE)
        )
        if URLMap.get_short(short_url_postfix):
            URLMap.get_unique_short_id()
        return short_url_postfix

    @staticmethod
    def get_short(short):
        """Получить объект по постфиксу короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_short_or_404(short):
        """Получить объект по постфиксу короткой ссылки. Или получить 404"""
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def create(original, short=None):
        """Создать объект в БД."""
        if short in [None, ""]:
            short = URLMap.get_unique_short_id()
        if not fullmatch(PATTERN, short):
            raise ValueError(PATTERN_ERROR)
        original_user_len = len(original)
        short_user_len = len(short)
        if original_user_len > ORIGINAL_MAX_LEN:
            raise ValueError(
                ORIGINAL_LEN_ERROR.format(ORIGINAL_MAX_LEN, original_user_len)
            )
        if short_user_len > SHORT_MAX_LEN:
            raise ValueError(
                SHORT_LEN_ERROR.format(SHORT_MAX_LEN, short_user_len)
            )
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
