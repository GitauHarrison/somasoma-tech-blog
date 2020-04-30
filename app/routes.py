from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have requested for user {}, remember_me{} to join Somasoma'.format(form.username.data, form.remember_me.data))
        redirect(url_for('index'))
    return render_template('login.html', title='Join Now', form=form)
