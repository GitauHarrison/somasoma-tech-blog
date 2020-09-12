from app import app
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm
from app.models import User, Post
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(username = form.username.data).first()
        if user is None and  not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember_me = form.remember_me.data)
        next_page = request.args.get('next')        
        if not next_page or url_parse(next_page).netloc() == '':
            next_page = url_for('home')
        return redirect(url_for(next_page))
    return render_template('login.html', title = 'Log In', form = form)