from app import db, login
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))

# Admin


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'Admin: {self.username}'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Anonymous User


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    comment = db.Column(db.String(140))

    comments = db.relationship(
        'AnonymousTemplateInheritanceComment',
        backref='author',
        lazy='dynamic'
        )

    def __repr__(self):
        return f'User: {self.name}'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# ============================================================
# ANONYMOUS COURSE CONTENT
# ============================================================


class AnonymousTemplateInheritanceComment(db.Model):
    __tablename__ = 'template inheritance comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Template Inheritance Comment: {self.body}'

# ============================================================
# ANONYMOUS COURSE CONTENT
# ============================================================