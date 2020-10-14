import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='<my_userame>'
    MAIL_PASSWORD='<my_password>'
    ADMINS=['<admin_email>']

    POSTS_PER_PAGE=10

    STRIPE_PUBLISHABLE_KEY='<stripe_publishable_key>'
    STRIPE_SECRET_KEY='<stripe_secret_key>'
    STRIPE_ENDPOINT_SECRET='<stripe_endpoint>'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
