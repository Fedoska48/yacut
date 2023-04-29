from flask import flash, redirect, render_template

from yacut import app
from yacut.error_handlers import UniqueGenerationError
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
    if not short:
        short = URLMap.get_unique_short()
    try:
        url_map = URLMap.create(form.original_link.data, short)
    except ValueError:
        flash(ALREADY_EXISTS_MAIN.format(short))
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short_url=URLMap.get_short_url(url_map.short)
    )


@app.route('/<string:short>')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    return redirect(URLMap.get_url_map_or_404(short).original)
