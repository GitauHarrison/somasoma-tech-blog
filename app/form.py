from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    submit = SubmitField('Join Now')