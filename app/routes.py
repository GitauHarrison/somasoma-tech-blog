from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')            
            return redirect(url_for('index'))
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Join Now', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/blog')
@login_required
def blog():
   # login_form = LoginForm()
   # register_form = RegistrationForm()
   # return render_template('login.html', title='Home', form = login_form, form = register_form)
   pass