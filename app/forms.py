from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
#from email_validator import validate_email, EmailNotValidError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Join Now')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CommentsForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    comment = TextAreaField('Comment', validators = [Length(min = 0, max = 140)])
    submit = SubmitField('Post Your comment')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reqest Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

#class PurchaseForm(FlaskForm):
    #payment_method = StringField('Payment Method', validators = [DataRequired()])
    #card_number = IntegerField('Card Number', validators = [DataRequired()])
    #expiry_date = 