from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from app.models import Admin
from flask_wtf.file import FileField


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
    remember_me = BooleanField('Remember Me')
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
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    confirm_password = PasswordField(
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


class UpdateBlogForm(FlaskForm):
    img = FileField('Update Blog Image')
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    submit = SubmitField('Update')


class UpdateEventsForm(FlaskForm):
    img = FileField('Update Events Image')
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    event_date = StringField(
        'Event Date',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={'placeholder': 'Thursday, December 23, 2021'}
        )
    event_time = StringField(
        'Event Time',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={'placeholder': '6.00 PM - 8.00 PM EAT'}
        )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    meet_link = StringField(
        'Meet Link',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    submit = SubmitField('Update')


class UpdateCoursesForm(FlaskForm):
    img = FileField('Update Courses Image')
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    overview = TextAreaField(
        'Overview',
        validators=[DataRequired()]
    )
    next_class_date = StringField(
        'Next Class Date',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    submit = SubmitField('Update')


class StudentStoriesForm(FlaskForm):
    img = FileField('Update Student Stories Image')
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    submit = SubmitField('Update')
