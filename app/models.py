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

    blogs = db.relationship(
        'UpdateBlog',
        backref='author',
        lazy='dynamic'
        )
    events = db.relationship(
        'UpdateEvents',
        backref='author',
        lazy='dynamic'
        )
    courses = db.relationship(
        'UpdateCourses',
        backref='author',
        lazy='dynamic'
        )

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
# END OF ANONYMOUS COURSE CONTENT
# ============================================================

# ============================================================
# ADMIN MANAGEMENT
# ============================================================


class UpdateBlog(db.Model):
    __tablename__ = 'update blog'
    id = db.Column(db.Integer, primary_key=True)
    blog_image = db.Column(db.String(140))
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(140))
    link = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Update Blog: {self.title}'


class UpdateEvents(db.Model):
    __tablename__ = 'update events'
    id = db.Column(db.Integer, primary_key=True)
    event_image = db.Column(db.String(140))
    event_date = db.Column(db.String(140))
    event_time = db.Column(db.String(140))
    location = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    link = db.Column(db.String(140))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Update Events: {self.body}'


class UpdateCourses(db.Model):
    __tablename__ = 'update course'
    id = db.Column(db.Integer, primary_key=True)
    course_image = db.Column(db.String(140))
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(140))
    overview = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    next_class_date = db.Column(db.String(140))
    link = db.Column(db.String(140))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Update Course: {self.title}'

# ============================================================
# ADMIN MANAGEMENT
# ============================================================
