from flask import jsonify, request

from yacut import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap

# Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_shortlink():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if 'original' not in data:
        raise InvalidAPIUsage('Отсутствуют обязательные поля')
    if 'short' not in data:
        data['short'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['short']).first() is not None:
        raise InvalidAPIUsage('Такая короткая ссылка уже существует')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url_map': url_map.to_dict()}), 201


# @app.route('/api/id/<short_id>/', methods=['GET'])
# def get_original_link(short_id):
#     """Получение оригинальной ссылки по указанному короткому идентификатору."""
#     pass
