from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm, RegistrationForm,EditProfileForm, ResetPasswordRequest, ResetPasswordForm, CommentsForm
from app.models import User
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from datetime import datetime
from app.emails import send_password_reset_email

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))        
        login_user(user, remember = form.remember_me.data)
        flash('You have successfully logged into your account')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title = 'Log In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully been registered. Please log in to access your account')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', title = 'Chat', user = user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods = ['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    user = User.query.filter_by(username = form.username.data)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data     
        db.session.commit()
        flash('You changes have been saved')
        return redirect(url_for('user', username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', user = user, title = 'Edit Profile', form = form)

@app.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions on how to reset your password')
        return redirect(url_for('login'))
    return render_template('request_password_reset.html', title = 'Request New Password', form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return render_template(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not User:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form = form, title = 'Reset Password')

@app.route('/discover')
def discover():
    return render_template('discover.html', title = 'Discover Courses')

@app.route('/blog')
def blog():
    return render_template('blog.html', title = 'Blog')

@app.route('/arduino')
def arduino():
    return render_template('arduino.html', title = 'Arduino')

@app.route('/quadcopter', methods = ['GET', 'POST'])
def quadcopter():
    form = CommentsForm()
    return render_template('quadcopter.html', title = 'Quadcopter', form = form)