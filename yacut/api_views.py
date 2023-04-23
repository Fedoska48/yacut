from flask import jsonify, request

from yacut import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap

# Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_shortlink_api():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if 'original_link' not in data:
        raise InvalidAPIUsage('Отсутствуют обязательные поля')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Такая короткая ссылка уже существует')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url_map': url_map.to_dict()}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage('Данные отсутствуют', 404)
