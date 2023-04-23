from flask import flash, redirect, render_template

from settings import ALREADY_EXISTS_MAIN, DOMAIN
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    """Страница генерации новой ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        else:
            custom_id = form.custom_id.data
            if URLMap.query.filter_by(short=custom_id).first():
                flash(ALREADY_EXISTS_MAIN.format(custom_id), 'unique-short')
                return render_template('index.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        custom_id = URLMap.query.get_or_404(url.id)
        return render_template(
            'index.html',
            form=form,
            url_link=DOMAIN + custom_id.short
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    url_object = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_object.original)
