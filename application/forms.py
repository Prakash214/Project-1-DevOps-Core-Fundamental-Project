from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Enter')

class AnimeForm(FlaskForm):
    anime_name = StringField('Anime Name', validators=[DataRequired(), Length(min=1, max=20)])
    anime_desc = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=100)])
    anime_status = SelectField('Anime Status', choices=[('ongoing', 'ongoing'), ('finished', 'finished')])
    released_date = DateField('Released Date', validators=[DataRequired("Please choose a date i")])
    assigned_to = SelectField('Assign To', choices=[])
    submit = SubmitField('Enter')