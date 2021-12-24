from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import AnonymousCommentForm, LoginForm, RegisterForm,\
    UpdateBlogForm, UpdateEventsForm, UpdateCoursesForm, StudentStoriesForm
from app.models import AnonymousTemplateInheritanceComment, User, Admin,\
    UpdateBlog, UpdateEvents, UpdateCourses, UpdateStudentStories
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.utils import secure_filename
import os


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
    page = request.args.get('page', 1, type=int)
    allowed_courses = UpdateCourses.query.filter_by(
        allowed_status=True).order_by(UpdateCourses.timestamp.desc()).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'courses',
        _anchor='courses-offerings',
        page=allowed_courses.next_num) \
        if allowed_courses.has_next else None
    prev_url = url_for(
        'courses',
        _anchor='courses-offerings',
        page=allowed_courses.prev_num) \
        if allowed_courses.has_prev else None
    return render_template(
        'courses.html',
        title='Courses',
        allowed_courses=allowed_courses.items,
        next_url=next_url,
        prev_url=prev_url
        )


@app.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    allowed_events = UpdateEvents.query.filter_by(
        allowed_status=True).order_by(UpdateEvents.timestamp.desc()).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'events',
        _anchor='events',
        page=allowed_events.next_num) \
        if allowed_events.has_next else None
    prev_url = url_for(
        'events',
        _anchor='events',
        page=allowed_events.prev_num) \
        if allowed_events.has_prev else None
    return render_template(
        'events.html',
        title='Events',
        allowed_events=allowed_events.items,
        next_url=next_url,
        prev_url=prev_url
        )

# =================================
# BLOG ROUTES
# =================================


@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    allowed_blogs = UpdateBlog.query.filter_by(
        allowed_status=True).order_by(
        UpdateBlog.timestamp.desc()).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'blog',
        _anchor="blogs",
        page=allowed_blogs.next_num) \
        if allowed_blogs.has_next else None
    prev_url = url_for(
        'blog',
        _anchor="blogs",
        page=allowed_blogs.prev_num) \
        if allowed_blogs.has_prev else None
    return render_template(
        'blog.html',
        title='Blog',
        allowed_blogs=allowed_blogs.items,
        next_url=next_url,
        prev_url=prev_url
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


@app.route('/blog/update', methods=['GET', 'POST'])
@login_required
def blog_update():
    form = UpdateBlogForm()
    if form.validate_on_submit():
        blog = UpdateBlog(
            title=form.title.data,
            body=form.body.data,
            link=form.link.data
            )

        # Handling file upload
        uploaded_file = form.blog_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])
        blog_image_path = os.path.join(
            app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', blog_image_path)
        uploaded_file.save(blog_image_path)
        blog.blog_image = blog_image_path
        print('Db path: ', blog.blog_image)

        blog_image_path_list = blog.blog_image.split('/')[1:]
        print('Img path list: ', blog_image_path_list)
        new_blog_image_path = '/'.join(blog_image_path_list)
        print('New img path: ', new_blog_image_path)
        blog.blog_image = new_blog_image_path
        print(blog.blog_image)

        db.session.add(blog)
        db.session.commit()
        flash('Your blog has been updated. Take action now!')
        return redirect(url_for('blog_update'))
    return render_template(
        'admin/update_blog.html',
        title='Blog Update',
        form=form
        )


@app.route('/blog/review')
@login_required
def blog_review():
    page = request.args.get('page', 1, type=int)
    blogs = UpdateBlog.query.order_by(
        UpdateBlog.timestamp.desc()
        ).paginate(
            page,
            app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'blog_review',
        page=blogs.next_num,
        _anchor="blog") \
        if blogs.has_next else None
    prev_url = url_for(
        'blog_review',
        page=blogs.prev_num,
        _anchor="blog") \
        if blogs.has_prev else None
    all_blogs = len(UpdateBlog.query.all())
    return render_template(
        'admin/review_blog.html',
        title='Blog Review',
        blogs=blogs.items,
        next_url=next_url,
        prev_url=prev_url,
        all_blogs=all_blogs
        )


@app.route('/blog/<int:id>/delete')
def blog_delete(id):
    blog = UpdateBlog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash(f'Blog {id} has been deleted.')
    return redirect(url_for('blog_review'))


@app.route('/blog/<id>/allow')
def blog_allow(id):
    blog = UpdateBlog.query.get_or_404(id)
    blog.allowed_status = True
    db.session.add(blog)
    db.session.commit()
    flash(f'Blog {id} has been approved.')
    return redirect(url_for('blog_review'))


@app.route('/events/update', methods=['GET', 'POST'])
@login_required
def events_update():
    form = UpdateEventsForm()
    if form.validate_on_submit():
        event = UpdateEvents(
            title=form.title.data,
            event_date=form.event_date.data,
            body=form.body.data,
            event_time=form.event_time.data,
            location=form.location.data,
            link=form.meet_link.data
            )

        # Handling file upload
        uploaded_file = form.event_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])
        event_image_path = os.path.join(
            app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', event_image_path)
        uploaded_file.save(event_image_path)
        event.event_image = event_image_path
        print('Db path: ', event.event_image)

        event_image_path_list = event.event_image.split('/')[1:]
        print('Img path list: ', event_image_path_list)
        new_event_image_path = '/'.join(event_image_path_list)
        print('New img path: ', new_event_image_path)
        event.event_image = new_event_image_path
        print(event.event_image)

        db.session.add(event)
        db.session.commit()
        flash('Your events has been updated. Take action now!')
        return redirect(url_for('events_update'))
    return render_template(
        'admin/update_events.html',
        title='Events Update',
        form=form
        )


@app.route('/events/review')
@login_required
def events_review():
    page = request.args.get('page', 1, type=int)
    events = UpdateEvents.query.order_by(
        UpdateEvents.timestamp.desc()
        ).paginate(
            page,
            app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'events_review',
        page=events.next_num,
        _anchor="events") \
        if events.has_next else None
    prev_url = url_for(
        'events_review',
        page=events.prev_num,
        _anchor="events") \
        if events.has_prev else None
    all_events = len(UpdateEvents.query.all())
    return render_template(
        'admin/review_events.html',
        title='Events Review',
        events=events.items,
        next_url=next_url,
        prev_url=prev_url,
        all_events=all_events
        )


@app.route('/events/<int:id>/delete')
def events_delete(id):
    event = UpdateEvents.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event {id} has been deleted.')
    return redirect(url_for('events_review'))


@app.route('/events/<id>/allow')
def events_allow(id):
    event = UpdateEvents.query.get_or_404(id)
    event.allowed_status = True
    db.session.add(event)
    db.session.commit()
    flash(f'Event {id} has been approved.')
    return redirect(url_for('events_review'))


@app.route('/student-stories/update', methods=['GET', 'POST'])
@login_required
def student_stories_update():
    form = StudentStoriesForm()
    return render_template(
        'admin/update_student_stories.html',
        title='Student Stories Update',
        form=form
        )


@app.route('/student-stories/review')
@login_required
def student_stories_review():
    return render_template(
        'admin/review_student_stories.html',
        title='Student Stories Review'
        )


@app.route('/courses/update', methods=['GET', 'POST'])
@login_required
def courses_update():
    form = UpdateCoursesForm()
    if form.validate_on_submit():
        course = UpdateCourses(
            title=form.title.data,
            body=form.body.data,
            overview=form.overview.data,
            next_class_date=form.next_class_date.data,
            link=form.link.data
            )

        # Handling file upload
        uploaded_file = form.course_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])
        course_image_path = os.path.join(
            app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', course_image_path)
        uploaded_file.save(course_image_path)
        course.course_image = course_image_path
        print('Db path: ', course.course_image)

        course_image_path_list = course.course_image.split('/')[1:]
        print('Img path list: ', course_image_path_list)
        new_course_image_path = '/'.join(course_image_path_list)
        print('New img path: ', new_course_image_path)
        course.course_image = new_course_image_path
        print(course.course_image)

        db.session.add(course)
        db.session.commit()
        flash('Your course has been updated. Take action now!')
        return redirect(url_for('courses_update'))
    return render_template(
        'admin/update_courses.html',
        title='Courses Update',
        form=form
        )


@app.route('/courses/review')
@login_required
def courses_review():
    page = request.args.get('page', 1, type=int)
    courses = UpdateCourses.query.order_by(
        UpdateCourses.timestamp.desc()
        ).paginate(
            page,
            app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'courses_review',
        page=courses.next_num,
        _anchor="courses") \
        if courses.has_next else None
    prev_url = url_for(
        'courses_review',
        page=courses.prev_num,
        _anchor="courses") \
        if courses.has_prev else None
    all_courses = len(UpdateCourses.query.all())
    return render_template(
        'admin/review_courses.html',
        title='Courses Review',
        courses=courses.items,
        next_url=next_url,
        prev_url=prev_url,
        all_courses=all_courses
        )


@app.route('/courses/<int:id>/delete')
def courses_delete(id):
    course = UpdateCourses.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash(f'Course {id} has been deleted.')
    return redirect(url_for('courses_review'))


@app.route('/courses/<id>/allow')
def courses_allow(id):
    course = UpdateCourses.query.get_or_404(id)
    course.allowed_status = True
    db.session.add(course)
    db.session.commit()
    flash(f'Course {id} has been approved.')
    return redirect(url_for('courses_review'))

# =================================
# END OF BLOG MANAGEMENT ROUTES
# =================================
