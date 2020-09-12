from flask import render_template
from app import app, db

@app.errorhandler(404)
def page_not_error(error):
    return render_template('404.html', title = 'Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title = 'Internal Error'), 500