from flask import jsonify, request

from yacut import app

from .error_handlers import InvalidAPIUsage
from .models import URLMap


NO_DATA = 'Отсутствует тело запроса'
REQUIRED_URL_FIELD = '"url" является обязательным полем!'
SHORT_ID_NOT_EXISTS = 'Указанный id не найден'
ALREADY_EXISTS_API = 'Имя "{}" уже занято.'

@app.route('/api/id/', methods=['POST'])
def create_shortlink_api():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_URL_FIELD)
    short = data.get('custom_id')
    # для api_views и views поднимаются разные сообщения после проверки ниже
    # т.е. если эту проверку положить внутрь create, то автотесты не пропустят
    try:
        url_map = URLMap.create(data['url'], short)
    except ValueError:
        raise InvalidAPIUsage(ALREADY_EXISTS_API.format(short))
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    url_map = URLMap.get_short_id(short_id)
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage(SHORT_ID_NOT_EXISTS, 404)
