import random
import string

from flask import abort, flash, redirect, render_template, url_for

from settings import URL_POSTFIX_SIZE
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def create_shortlink():
    form = URLMapForm()
    if form.validate_on_submit():
        url = URLMap(
            original=form.original.data,
            short=form.short.data,
        )
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('url_view', id=url.id))
    return render_template('index.html', form=form)


@app.route('/url/<int:id>/')
def url_view(id):
    url_link = URLMap.query.get_or_404(id)
    return render_template('url_view.html', url_link=url_link)


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_url_postfix = ''.join(
        random.sample(letters_and_digits, URL_POSTFIX_SIZE)
    )
    return short_url_postfix
