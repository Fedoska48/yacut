from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired, Length, Optional, ValidationError, Regexp
)

from yacut.constants import SHORT_MAX_LEN, PATTERN_SYMBOLS
from yacut.models import ORIGINAL_MAX_LEN, PATTERN_ERROR, URLMap

ORIGINAL_LINK_FIELD_TEXT = 'Вставьте ссылку для обработки'
CUSTOM_ID_FIELD_TEXT = 'Вариант короткой ссылки'
REQIURED_FIELD_TEXT = 'Обязательное поле'
SUBMIT_TEXT = 'Создать'
ALREADY_EXISTS_FORM = 'Имя {} уже занято!'


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
        validators=[
            Length(max=SHORT_MAX_LEN),
            Optional(),
            Regexp(PATTERN_SYMBOLS, message=PATTERN_ERROR)
        ]
    )
    submit = SubmitField(SUBMIT_TEXT)

    def validate_custom_id(self, custom_id):
        short = self.custom_id.data
        if URLMap.get_url_map(short):
            raise ValidationError(ALREADY_EXISTS_FORM.format(short))
