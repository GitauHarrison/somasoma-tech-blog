from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
mail = Mail(app)
moment = Moment(app)

from app import routes, models, errors
