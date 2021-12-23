from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import AnonymousCommentForm, LoginForm, RegisterForm,\
    UpdateBlogForm, UpdateEventsForm, UpdateCoursesForm, StudentStoriesForm
from app.models import AnonymousTemplateInheritanceComment, User, Admin
from flask_login import current_user, login_required, logout_user, login_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('login'))
    return render_template(
        'admin/register.html',
        title='Admin Register',
        form=form
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(admin, remember=form.remember_me.data)
        flash(f'Welcome back, {admin.username}')
        return redirect(url_for('dashboard'))
    return render_template(
        'admin/login.html',
        title='Admin Login',
        form=form
        )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard'
        )


@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'home.html',
        title='Home'
        )


@app.route('/courses')
def courses():
    return render_template(
        'courses.html',
        title='Courses'
        )


@app.route('/events')
def events():
    return render_template(
        'events.html',
        title='Events'
        )

# =================================
# BLOG ROUTES
# =================================


@app.route('/blog')
def blog():
    return render_template(
        'blog.html',
        title='Blog'
        )


@app.route('/blog/template-inheritance', methods=['GET', 'POST'])
def blog_template_inheritance():
    form = AnonymousCommentForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        comment = AnonymousTemplateInheritanceComment(
            body=form.comment.data,
            author=user
            )
        db.session.add(comment)
        db.session.add(user)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for(
            'blog_template_inheritance',
            _anchor='comments'))
    page = request.args.get('page', 1, type=int)
    comments = AnonymousTemplateInheritanceComment.query.order_by(
        AnonymousTemplateInheritanceComment.timestamp.desc()
        ).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'blog_template_inheritance',
        page=comments.next_num,
        _anchor="comments") \
        if comments.has_next else None
    prev_url = url_for(
        'blog_template_inheritance',
        page=comments.prev_num,
        _anchor="comments") \
        if comments.has_prev else None
    all_comments = len(AnonymousTemplateInheritanceComment.query.all())
    return render_template(
        'blogs/template_inheritance.html',
        title='Template Inheritance',
        form=form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments
        )

# =================================
# END OF BLOG ROUTES
# =================================

# =================================
# COURSES ROUTES
# =================================


@app.route('/courses/flask')
def flask():
    return render_template(
        'course_flask.html',
        title='Flask'
        )


@app.route('/courses/python-dsa')
def python_dsa():
    return render_template(
        'course_python_dsa.html',
        title='Python-DSA'
        )


@app.route('/courses/data-science')
def data_science():
    return render_template(
        'course_data_science.html',
        title='Data Science'
        )


@app.route('/courses/machine-learning')
def machine_learning():
    return render_template(
        'course_machine_learning.html',
        title='Machine Learning'
        )

# =================================
# END OF COURSES ROUTES
# =================================


# =================================
# BLOG MANAGEMENT ROUTES
# =================================


@app.route('/blog/update')
def blog_update():
    form = UpdateBlogForm()
    return render_template(
        'admin/update_blog.html',
        title='Blog Update',
        form=form
        )


@app.route('/blog/review')
def blog_review():
    return render_template(
        'admin/review_blog.html',
        title='Blog Review'
        )


@app.route('/events/update')
def events_update():
    form = UpdateEventsForm()
    return render_template(
        'admin/update_events.html',
        title='Events Update',
        form=form
        )


@app.route('/events/review')
def events_review():
    return render_template(
        'admin/review_events.html',
        title='Events Review'
        )


@app.route('/student-stories/update')
def student_stories_update():
    form = StudentStoriesForm()
    return render_template(
        'admin/update_student_stories.html',
        title='Student Stories Update',
        form=form
        )


@app.route('/student-stories/review')
def student_stories_review():
    return render_template(
        'admin/review_student_stories.html',
        title='Student Stories Review'
        )


@app.route('/courses/update')
def courses_update():
    form = UpdateCoursesForm()
    return render_template(
        'admin/update_courses.html',
        title='Courses Update',
        form=form
        )


@app.route('/courses/review')
def courses_review():
    return render_template(
        'admin/review_courses.html',
        title='Courses Review'
        )

# =================================
# END OF BLOG MANAGEMENT ROUTES
# =================================
