import random
from datetime import datetime
from re import fullmatch

from flask import url_for

from yacut import db
from yacut.constants import (SYMBOLS, RECURSION_ATTEMPT, ORIGINAL_MAX_LEN,
                             PATTERN, SHORT_MAX_LEN, URL_POSTFIX_SIZE,
                             URL_ROUTING_VIEW)
from yacut.error_handlers import InvalidAPIUsage

# messages
PATTERN_ERROR = 'Указано недопустимое имя для короткой ссылки'
ORIGINAL_LEN_ERROR = ('Длинна входной ссылки должна быть менее {} символов.'
                      'Ваш  размер: {}')
SHORT_LEN_ERROR = ('Вариант короткой ссылки должен быть не больше {} символов.'
                   'Ваш размер: {}')


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

    def from_dict(self, data):
        """Преобразование словаря в объект модели (JSON -> словарь).
        В пустой объект класса URLMap добавляются поля полученные в POST."""
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def get_unique_short_id(_recursion_attempt=RECURSION_ATTEMPT):
        """Генератор шестизначного постфикса для ссылки."""
        short_url_postfix = ''.join(
            random.sample(SYMBOLS, URL_POSTFIX_SIZE)
        )
        if URLMap.get_short_id(short_url_postfix):
            for _ in range(_recursion_attempt):
                URLMap.get_unique_short_id()
        return short_url_postfix

    @staticmethod
    def get_short_id(short):
        """Получить объект по постфиксу короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_short_id_or_404(short):
        """Получить объект по постфиксу короткой ссылки. Или получить 404"""
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get_short_url(postfix):
        return url_for(URL_ROUTING_VIEW, short=postfix, _external=True)

    @staticmethod
    def create(original, short=None):
        """Создать объект в БД."""
        if short in [None, ""]:
            short = URLMap.get_unique_short_id()
        original_user_len = len(original)
        # проверка длины для данных из API интерфейса
        if original_user_len > ORIGINAL_MAX_LEN:
            raise ValueError(
                ORIGINAL_LEN_ERROR.format(ORIGINAL_MAX_LEN, original_user_len)
            )
        # размер проверяем через регулярку
        # уникальность приходится проверят вне метода из-за ТЗ в автотестах
        # разничный текст должен подниматься во views и api_views
        if URLMap.get_short_id(short) is not None:
            raise ValueError()
        if not fullmatch(PATTERN, short):
            # проверкой на соответствие в этом месте,отсекаем проверку "пустых"
            # значений. Мне кажется, лучше проверить финальное значение,
            # чем проверять пустоту или выводить пустоту из под проверки
            raise InvalidAPIUsage(PATTERN_ERROR)
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
