import random
from datetime import datetime
from re import fullmatch

from flask import url_for

from yacut import db
from yacut.constants import (
    CREATE_UNIQUE_ATTEMPT, ORIGINAL_MAX_LEN, PATTERN_SYMBOLS, SHORT_MAX_LEN,
    SYMBOLS, URL_POSTFIX_SIZE, URL_ROUTING_VIEW
)
from yacut.error_handlers import UniqueGenerationError, UniqueValidationError

# messages
PATTERN_ERROR = 'Указано недопустимое имя для короткой ссылки'
ORIGINAL_LEN_ERROR = (f'Длинна входной ссылки должна быть менее '
                      f'{ORIGINAL_MAX_LEN} символов.'
                      'Ваш  размер: {}')
GENERATION_ERROR = ('Проблема уникальности при генерации ссылки. '
                    'Повторите попытку.')
ALREADY_EXISTS = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(ORIGINAL_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LEN), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразование объекта модели в словарь (словарь -> JSON)."""
        return dict(
            url=self.original,
            short_link=URLMap.get_short_url(self.short)
        )

    @staticmethod
    def get_unique_short(attempt=CREATE_UNIQUE_ATTEMPT):
        """Генератор short случайным образом из латинских букв и чисел."""
        for _ in range(attempt):
            short = ''.join(
                random.sample(SYMBOLS, URL_POSTFIX_SIZE)
            )
            if not URLMap.get_url_map(short):
                return short
        raise UniqueGenerationError(GENERATION_ERROR)

    @staticmethod
    def get_url_map(short):
        """Получить объект по постфиксу короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_url_map_or_404(short):
        """Получить объект по постфиксу короткой ссылки. Или получить 404"""
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get_short_url(short):
        return url_for(URL_ROUTING_VIEW, short=short, _external=True)

    @staticmethod
    def create(original, short=None, validate=False):
        """Создать объект в БД."""
        original_user_len = len(original)
        # необходимо валидировать урл, который не прошел через форму: АПИшный
        # два случая: с пустой коротюлькой и заполненной. Оба с флагом True
        # если пустая - генерируем коротюльку, переставляем флаг на False,
        # но как-то надо валидировать длинную ссылку в этом случае,
        # либо 1) перехватывать тут чтобы сразу уходило на создание объекта
        # либо 2) валидировать в api_views до попадания в метод create
        # к тому же это "легкая" проверка без запросов в БД
        if original_user_len > ORIGINAL_MAX_LEN:
            raise ValueError(
                ORIGINAL_LEN_ERROR.format(original_user_len)
            )
        if short in [None, ""]:
            short = URLMap.get_unique_short()
            validate = False
        if validate:
            short_user_len = len(short)
            if short_user_len > SHORT_MAX_LEN:
                raise ValueError(PATTERN_ERROR)
            if not fullmatch(PATTERN_SYMBOLS, short):
                raise ValueError(PATTERN_ERROR)
            if URLMap.get_url_map(short):
                raise UniqueValidationError(ALREADY_EXISTS.format(short))
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
