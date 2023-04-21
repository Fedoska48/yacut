from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original = TextAreaField(
        'Вставьте ссылку для обработки',
        validators=[DataRequired(message='Обязательное поле')]
    )
    short = URLField(
        'Добавьте короткую ссылку, которую вы хотели бы получить',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Добавить')