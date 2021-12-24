import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or\
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Comments
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE') or 10)

    # Form
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # File upload
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH') or 'static/img/uploads'

    # Local testing
    START_NGROK = os.environ.get('START_NGROK') is not None

    # Heroku logs
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # Email Support
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
