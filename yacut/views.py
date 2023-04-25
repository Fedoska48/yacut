from flask import flash, redirect, render_template

from settings import DOMAIN
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap

VALIDATION_ERROR = 'Данные не прошли валидацию. Проверьте данные.'
ALREADY_EXISTS_MAIN = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    """Страница генерации новой ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.get_short(short):
            flash(ALREADY_EXISTS_MAIN.format(short))
            return render_template('index.html', form=form)
        URLMap.create(form.original_link.data, short)
        return render_template(
            'index.html',
            form=form,
            url_link=DOMAIN + short
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    return redirect(URLMap.get_short_or_404(short).original)
