from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField


class UpdateBlogForm(FlaskForm):
    blog_image = FileField('Blog Image')
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    submit = SubmitField('Update')


class UpdateEventsForm(FlaskForm):
    event_image = FileField('Events Image')
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    event_date = StringField(
        'Event Date',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'Thursday, December 23, 2021'}
        )
    event_time = StringField(
        'Event Time',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': '6.00 PM - 8.00 PM EAT'}
        )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    meet_link = StringField(
        'Meet Link',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    submit = SubmitField('Update')


class UpdateCoursesForm(FlaskForm):
    course_image = FileField(
        'Courses Image',
        validators=[DataRequired()]
        )
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=100)]
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
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'December 26, 2021'}
        )
    link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    submit = SubmitField('Update')


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
