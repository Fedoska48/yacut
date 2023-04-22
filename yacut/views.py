from flask import abort, flash, redirect, render_template, url_for

from settings import DOMAIN_PREFIX_LIST, FULL_SHORT_SIZE
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    """Страница генерации новой ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.short.data
        if not short:
            short = DOMAIN_PREFIX_LIST[0] + get_unique_short_id()
        else:
            if len(form.short.data) > FULL_SHORT_SIZE:
                flash(
                    f'Должно быть менее {FULL_SHORT_SIZE} символов!',
                    'unique-short'
                )
                return render_template('index.html', form=form)
            short = DOMAIN_PREFIX_LIST[0] + form.short.data
            if URLMap.query.filter_by(short=short).first():
                flash('Такая короткая ссылка уже существует!', 'unique-short')
                return render_template('index.html', form=form)
        url = URLMap(
            original=form.original.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        url_link = URLMap.query.get_or_404(url.id)
        return render_template('index.html', form=form, url_link=url_link)
    return render_template('index.html', form=form)

@app.route('/<string:short>/')
def url_routing(short):
    """Маршрутизация ссылки short в original."""
    url_object = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_object.original)
