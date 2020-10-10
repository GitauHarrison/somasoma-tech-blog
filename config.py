import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'Norules Anymore'
    MAIL_PASSWORD = 'Gu#DQrZb2Y_4K!6j'
    ADMINS = ['norulesanymore@gmail.com']

    POSTS_PER_PAGE = 10

    STRIPE_PUBLISHABLE_KEY=os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY=os.environ.get('STRIPE_SECRET_KEY')
