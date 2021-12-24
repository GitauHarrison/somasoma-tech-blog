from app import db
from app.errors import bp
from flask import render_template


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template(
        'errors/404.html',
        title='Page Not Found'
        ), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'errors/500.html',
        title='Internal Error'
        ), 500
