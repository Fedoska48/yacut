from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from yacut.models import SHORT_MAX_LEN, ORIGINAL_MAX_LEN

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
