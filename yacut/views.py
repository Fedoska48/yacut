import random
import string

from flask import render_template

from settings import URL_POSTFIX_SIZE
from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap


@app.route('/')
def create_shortlink():
    # url = URLMapForm()
    return render_template('index.html')


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_url_postfix = ''.join(
        random.sample(letters_and_digits, URL_POSTFIX_SIZE)
    )
    return short_url_postfix
