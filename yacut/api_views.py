from flask import jsonify, request

from yacut import app

from .error_handlers import InvalidAPIUsage, UniqueGenerationError
from .models import URLMap

NO_DATA = 'Отсутствует тело запроса'
REQUIRED_URL_FIELD = '"url" является обязательным полем!'
SHORT_NOT_EXISTS = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_shortlink_api():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_URL_FIELD)
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'), validate=True)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    except UniqueGenerationError as error:
        print(error)
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_link(short):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    url_map = URLMap.get_url_map(short)
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage(SHORT_NOT_EXISTS, 404)
