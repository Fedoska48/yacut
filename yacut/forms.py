from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from yacut.models import (ORIGINAL_MAX_LEN, SHORT_MAX_LEN, LETTERS_AND_DIGITS,
                          PATTERN_ERROR, URLMap)
from yacut.views import ALREADY_EXISTS_MAIN

ORIGINAL_LINK_FIELD_TEXT = 'Вставьте ссылку для обработки'
CUSTOM_ID_FIELD_TEXT = 'Вариант короткой ссылки'
REQIURED_FIELD_TEXT = 'Обязательное поле'
SUBMIT_TEXT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = TextAreaField(
        ORIGINAL_LINK_FIELD_TEXT,
        validators=[
            Length(max=ORIGINAL_MAX_LEN),
            DataRequired(message=REQIURED_FIELD_TEXT)
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_FIELD_TEXT,
        validators=[Length(max=SHORT_MAX_LEN), Optional()]
    )
    submit = SubmitField(SUBMIT_TEXT)

    def validate_custom_id(self):
        short = self.custom_id.data
        if URLMap.get_short(short):
            raise ValidationError(ALREADY_EXISTS_MAIN.format(short))
        for char in short:
            if char not in LETTERS_AND_DIGITS:
                raise ValidationError(PATTERN_ERROR)
