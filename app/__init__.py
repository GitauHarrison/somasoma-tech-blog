from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # def start_ngrok():
    #     from pyngrok import ngrok

    #     url = ngrok.connect(5000)
    #     print('* Tunnel URL: *', url)

    # if current_app.config['START_NGROK']:
    #     start_ngrok()

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models
