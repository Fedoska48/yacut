from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = TextAreaField(
        'Вставьте ссылку для обработки',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
