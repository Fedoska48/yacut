from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

from yacut import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap

# Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml
from .utils import get_unique_short_id

PATTERN = r'^[a-zA-Z0-9]{1,16}$'


@app.route('/api/id/', methods=['POST'])
def create_shortlink_api():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' in data:
        if 'custom_id' not in data or not data['custom_id']:
            data['custom_id'] = get_unique_short_id()
        elif URLMap.query.filter_by(
                short=data['custom_id']
        ).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
        elif not fullmatch(PATTERN, data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
            )
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return jsonify(url_map.to_dict()), 201
    raise InvalidAPIUsage('"url" является обязательным полем!')


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
