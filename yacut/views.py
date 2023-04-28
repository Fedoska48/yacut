from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.error_handlers import InvalidUsage
from yacut.forms import URLMapForm
from yacut.models import URLMap

ALREADY_EXISTS_MAIN = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    """Страница генерации новой ссылки."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    # для api_views и views поднимаются разные сообщения после проверки ниже
    # т.е. если эту проверку положить внутрь create, то автотесты не пропустят
    if URLMap.get_short(short):
        flash(ALREADY_EXISTS_MAIN.format(short))
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, short)
    except ValueError as error:
        raise InvalidUsage(error)
    return render_template(
        'index.html',
        form=form,
        url_link=URLMap.get_short_url(url_map.short)
    )


@app.route('/<string:short>')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    return redirect(URLMap.get_short_or_404(short).original)
