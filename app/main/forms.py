from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField


class AnonymousCommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=100)]
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


class StudentStoriesForm(FlaskForm):
    student_image = FileField('Student Image')
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    submit = SubmitField('Update')
