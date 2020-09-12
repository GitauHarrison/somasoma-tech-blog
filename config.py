import os, smtplib

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configurations
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME ="Taste Bolder"
    MAIL_PASSWORD ="d$x8&ty29^w*#C7F"
    ADMINS = ['tastebolder@gmail.com']

    LANGUAGES = ['en', 'sw']