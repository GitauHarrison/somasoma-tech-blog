from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from app.models import Admin


# Anonymous Comment form


class AnonymousCommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
        )
    comment = TextAreaField(
        'Comment',
        validators=[DataRequired()]
        )
    submit = SubmitField('Post')


# Admin


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    password = StringField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
        )
    password = StringField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    confirm_password = StringField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
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
