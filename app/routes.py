from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for {}, remember me = {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html', title = 'Log In', form = form)