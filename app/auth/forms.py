from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from app.models import Admin


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            EqualTo('password')
            ]
        )
    submit = SubmitField('Register')

    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin is not None:
            raise ValidationError('Please use a different email address.')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            EqualTo('password')
            ]
        )
    submit = SubmitField('Reset Password')
