from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username (self, username):
        user = User.query.filter_by(username = username.data)
        if user is not None:
            raise ValidationError('Please use a different username')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data)
        if user is not None:
            raise ValidationError('Please use a different email address')