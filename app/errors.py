from app import app, db
from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'errors/404.html',
        title='Page Not Found'
        ), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'errors/500.html',
        title='Internal Error'
        ), 500
