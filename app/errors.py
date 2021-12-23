from app import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title='Internal Error'), 500