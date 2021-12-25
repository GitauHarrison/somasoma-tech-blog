from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from flask import render_template, redirect, url_for, flash
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm,\
    RequestPasswordResetForm
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


@bp.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin:
            send_password_reset_email(admin)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/request_password_reset.html',
        form=form,
        title='Request Password Reset'
        )


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    admin = Admin.verify_reset_password_token(token)
    if not admin:
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        admin.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/reset_password.html',
        form=form,
        title='Reset Password'
        )
