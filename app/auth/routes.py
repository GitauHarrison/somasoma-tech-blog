from app import db
from app.auth import bp
from flask import render_template, redirect, url_for, flash
from app.auth.forms import LoginForm, RegisterForm
from app.models import Admin
from flask_login import current_user, login_required, logout_user, login_user


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        admin = Admin(
            username=form.username.data,
            email=form.email.data
            )
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/register.html',
        title='Admin Register',
        form=form
        )


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(admin, remember=form.remember_me.data)
        flash(f'Welcome back, {admin.username}')
        return redirect(url_for('admin.dashboard'))
    return render_template(
        'auth/login.html',
        title='Admin Login',
        form=form
        )


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
