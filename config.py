import os

basedir = os.path.abspath(os.path.dirname(__file__))


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
