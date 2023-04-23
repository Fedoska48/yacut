from re import fullmatch

from flask import jsonify, request

from settings import (ALREADY_EXISTS_API, NO_DATA, PATTERN, PATTERN_ERROR,
                      REQUIRED_URL_FIELD, SHORT_ID_NOT_EXISTS)
from yacut import app, db

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_shortlink_api():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' in data:
        if 'custom_id' not in data or not data['custom_id']:
            data['custom_id'] = get_unique_short_id()
        elif URLMap.query.filter_by(
                short=data['custom_id']
        ).first() is not None:
            raise InvalidAPIUsage(ALREADY_EXISTS_API.format(data["custom_id"]))
        elif not fullmatch(PATTERN, data['custom_id']):
            raise InvalidAPIUsage(PATTERN_ERROR)
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return jsonify(url_map.to_dict()), 201
    raise InvalidAPIUsage(REQUIRED_URL_FIELD)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage(SHORT_ID_NOT_EXISTS, 404)
