from app import db
from app.main import bp
from flask import render_template, request, redirect, url_for, flash,\
    current_app
from app.main.forms import StudentStoriesForm, AnonymousCommentForm
from app.models import AnonymousTemplateInheritanceComment, User,\
    UpdateBlog, UpdateEvents, UpdateCourses, FlaskStudentStories,\
    DataScienceStudentStories
from werkzeug.utils import secure_filename
import os


@bp.route('/')
@bp.route('/home')
def home():
    return render_template(
        'home.html',
        title='Home'
        )


@bp.route('/courses')
def courses():
    page = request.args.get('page', 1, type=int)
    allowed_courses = UpdateCourses.query.filter_by(
        allowed_status=True).order_by(UpdateCourses.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.courses',
        _anchor='courses-offerings',
        page=allowed_courses.next_num) \
        if allowed_courses.has_next else None
    prev_url = url_for(
        'main.courses',
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


@bp.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    allowed_events = UpdateEvents.query.filter_by(
        allowed_status=True).order_by(UpdateEvents.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.events',
        _anchor='events',
        page=allowed_events.next_num) \
        if allowed_events.has_next else None
    prev_url = url_for(
        'main.events',
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


@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    allowed_blogs = UpdateBlog.query.filter_by(
        allowed_status=True).order_by(
        UpdateBlog.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.blog',
        _anchor="blogs",
        page=allowed_blogs.next_num) \
        if allowed_blogs.has_next else None
    prev_url = url_for(
        'main.blog',
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


@bp.route('/blog/template-inheritance', methods=['GET', 'POST'])
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
            'main.blog_template_inheritance',
            _anchor='comments'))
    page = request.args.get('page', 1, type=int)
    comments = AnonymousTemplateInheritanceComment.query.order_by(
        AnonymousTemplateInheritanceComment.timestamp.desc()
        ).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.blog_template_inheritance',
        page=comments.next_num,
        _anchor="comments") \
        if comments.has_next else None
    prev_url = url_for(
        'main.blog_template_inheritance',
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


@bp.route('/courses/flask')
def flask():
    page = request.args.get('page', 1, type=int)
    allowed_students = FlaskStudentStories.query.filter_by(
        allowed_status=True).order_by(
        FlaskStudentStories.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.flask',
        _anchor='student-stories',
        page=allowed_students.next_num) \
        if allowed_students.has_next else None
    prev_url = url_for(
        'main.flask',
        _anchor='student-stories',
        page=allowed_students.prev_num) \
        if allowed_students.has_prev else None
    return render_template(
        'course_flask.html',
        title='Flask',
        allowed_students=allowed_students.items,
        next_url=next_url,
        prev_url=prev_url
        )


@bp.route('/courses/data-science')
def data_science():
    return render_template(
        'course_data_science.html',
        title='Data Science'
        )


@bp.route('/flask/student-stories/form', methods=['GET', 'POST'])
def flask_student_stories_form():
    form = StudentStoriesForm()
    if form.validate_on_submit():
        student = FlaskStudentStories(
            username=form.username.data,
            body=form.body.data
            )

        # Handling file upload
        uploaded_file = form.student_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        student_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', student_image_path)
        uploaded_file.save(student_image_path)
        student.student_image = student_image_path
        print('Db path: ', student.student_image)

        student_image_path_list = student.student_image.split('/')[1:]
        print('Img path list: ', student_image_path_list)
        new_student_image_path = '/'.join(student_image_path_list)
        print('New img path: ', new_student_image_path)
        student.student_image = new_student_image_path
        print(student.student_image)

        db.session.add(student)
        db.session.commit()
        flash('Your student story has been saved. The admin will review it')
        return redirect(url_for('main.flask_student_stories_form'))
    return render_template(
        'blogs/student_stories_form.html',
        title='Student Stories',
        form=form
        )


@bp.route('/data-science/student-stories/form', methods=['GET', 'POST'])
def data_science_student_stories_form():
    form = StudentStoriesForm()
    if form.validate_on_submit():
        student = DataScienceStudentStories(
            username=form.username.data,
            body=form.body.data
            )

        # Handling file upload
        uploaded_file = form.student_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        student_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', student_image_path)
        uploaded_file.save(student_image_path)
        student.student_image = student_image_path
        print('Db path: ', student.student_image)

        student_image_path_list = student.student_image.split('/')[1:]
        print('Img path list: ', student_image_path_list)
        new_student_image_path = '/'.join(student_image_path_list)
        print('New img path: ', new_student_image_path)
        student.student_image = new_student_image_path
        print(student.student_image)

        db.session.add(student)
        db.session.commit()
        flash('Your student story has been saved. The admin will review it')
        return redirect(url_for('main.flask_student_stories_form'))
    return render_template(
        'blogs/student_stories_form.html',
        title='Student Stories',
        form=form
        )

# =================================
# END OF COURSES ROUTES
# =================================
