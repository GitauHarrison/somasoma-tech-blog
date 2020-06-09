from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm, RegistrationForm, CommentsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Comments
from werkzeug.urls import url_parse
from datetime import datetime

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
    return redirect(url_for('login'))

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
        return redirect(url_for('blog'))
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

@app.route('/quadcopter/<username>', methods = ['GET', 'POST'])
@login_required
def quadcopter(username):
    user = User.query.filter_by(username = username)
    form = CommentsForm()    
    comments = [
        {'author': username, 'body': form.comment.data}
    ]
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.body = form.comment.data
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('quadcopter'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('quadcopter.html', title = 'Quadcopter', form = form, user = user)

@app.route('/lead_the_field')
@login_required
def lead_the_field():
    return render_template('lead_the_field.html', title = 'Lead the Field')


#@app.route('/blog')
#@login_required
#def blog():
   # login_form = LoginForm()
   # register_form = RegistrationForm()
   # return render_template('login.html', title='Home', form = login_form, form = register_form)
   #pass