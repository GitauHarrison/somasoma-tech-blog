from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')