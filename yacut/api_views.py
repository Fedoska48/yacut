from yacut import app


# Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml

@app.route('/api/<int:id>/', methods=['POST'])
def create_shortlink():
    ...


@app.route('/api/<int:id>/<string:short_id>', methods=['GET'])
def get_original_link():
    ...
