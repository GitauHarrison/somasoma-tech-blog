from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm, RegistrationForm, CommentsForm, ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.email import send_password_reset_email

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')            
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':            
            next_page = url_for('quadcopter')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('discover'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation! You are now a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Join Now', form = form)

@app.route('/discover')
def discover():
    return render_template('discover.html', title = 'Discover')

@app.route('/blog')
def blog():
    return render_template('blog.html', title = 'Blog')

@app.route('/arduino')
def arduino():
    return render_template('arduino.html', title = 'Arduino')

@app.route('/quadcopter')
@login_required
def quadcopter():
    form = CommentsForm()
    return render_template('quadcopter.html', title = 'Quadcopter', form = form)

@app.route('/lead_the_field')
@login_required
def lead_the_field():
    return render_template('lead_the_field.html', title = 'Lead the Field')

@app.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions on how to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', form=form, title = 'Reset Password Request')

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('blog'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title = 'Reset Password', form = form)

#@app.route('/blog')
#@login_required
#def blog():
   # login_form = LoginForm()
   # register_form = RegistrationForm()
   # return render_template('login.html', title='Home', form = login_form, form = register_form)
   #pass