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
    MAIL_USERNAME='norulesanymore@gmail.com'
    MAIL_PASSWORD='Gu#DQrZb2Y_4K!6j'
    ADMINS=['norulesanymore@gmail.com']

    POSTS_PER_PAGE=10

    STRIPE_PUBLISHABLE_KEY='pk_test_51HaVXcFjP6O4anVpYtXKDnFyXevd0gQcTVZKKnliCz2PL3C1jU8G7H94uimc3xaEHJK5Cl40xfvF7o1nobSGh5zK00ecRRgijH'
    STRIPE_SECRET_KEY='sk_test_51HaVXcFjP6O4anVpX06vRtKSueLhkq4vf2vpVZcDqXcHJVkUVB4hy5GpOniQZZ3viDg6Qi4lZb41QmmpRF1PgYSt001nfeOlZJ'
    STRIPE_ENDPOINT_SECRET='whsec_wnJMeZIAWSHZm5sONh5eBP8pSmiWpcDp'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # DATABASE_URL = 'postgres://bwtllxapoeoivu:e24fd0f855787958be8348aec5f6eb588cea7ce410e5a026c344cf78b1463b5a@ec2-34-234-185-150.compute-1.amazonaws.com:5432/dc1q33b8qs0gmq'