from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap

VALIDATION_ERROR = 'Данные не прошли валидацию. Проверьте данные.'
ALREADY_EXISTS_MAIN = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    """Страница генерации новой ссылки."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    if URLMap.get_short(short):
        flash(ALREADY_EXISTS_MAIN.format(short))
        return render_template('index.html', form=form)
    url_map = URLMap.create(form.original_link.data, short)
    return render_template(
        'index.html',
        form=form,
        url_link=url_for('url_routing', short=url_map.short, _external=True)
    )


@app.route('/<string:short>')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    return redirect(URLMap.get_short_or_404(short).original)
