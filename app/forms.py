from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


# Anonymous Comment form


class AnonymousCommentForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)]
                       )
    email = StringField('Email',
                        validators=[DataRequired(), Email()]
                        )
    comment = TextAreaField('Comment',
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Post')
