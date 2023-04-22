import random
import string
from settings import URL_POSTFIX_SIZE


def get_unique_short_id():
    """Генератор шестизначного постфикса для ссылки."""
    letters_and_digits = string.ascii_letters + string.digits
    short_url_postfix = ''.join(
        random.sample(letters_and_digits, URL_POSTFIX_SIZE)
    )
    return short_url_postfix
