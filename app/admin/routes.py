from app import db
from app.admin import bp
from flask import render_template, request, redirect, url_for, flash,\
    current_app
from app.admin.forms import UpdateBlogForm, UpdateEventsForm,\
    UpdateCoursesForm
from app.models import UpdateBlog, UpdateEvents, UpdateCourses,\
    FlaskStudentStories, DataScienceStudentStories
from flask_login import login_required
from werkzeug.utils import secure_filename
import os


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard'
        )


# =================================
# BLOG MANAGEMENT ROUTES
# =================================

# Blog

@bp.route('/blog/update', methods=['GET', 'POST'])
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
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        blog_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
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
        return redirect(url_for('admin.blog_update'))
    return render_template(
        'admin/update_blog.html',
        title='Blog Update',
        form=form
        )


@bp.route('/blog/review')
@login_required
def blog_review():
    page = request.args.get('page', 1, type=int)
    blogs = UpdateBlog.query.order_by(
        UpdateBlog.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.blog_review',
        page=blogs.next_num,
        _anchor="blog") \
        if blogs.has_next else None
    prev_url = url_for(
        'admin.blog_review',
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


@bp.route('/blog/<int:id>/delete')
def blog_delete(id):
    blog = UpdateBlog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash(f'Blog {id} has been deleted.')
    return redirect(url_for('admin.blog_review'))


@bp.route('/blog/<id>/allow')
def blog_allow(id):
    blog = UpdateBlog.query.get_or_404(id)
    blog.allowed_status = True
    db.session.add(blog)
    db.session.commit()
    flash(f'Blog {id} has been approved.')
    return redirect(url_for('admin.blog_review'))

# Events


@bp.route('/events/update', methods=['GET', 'POST'])
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
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        event_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
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
        return redirect(url_for('admin.events_update'))
    return render_template(
        'admin/update_events.html',
        title='Events Update',
        form=form
        )


@bp.route('/events/review')
@login_required
def events_review():
    page = request.args.get('page', 1, type=int)
    events = UpdateEvents.query.order_by(
        UpdateEvents.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.events_review',
        page=events.next_num,
        _anchor="events") \
        if events.has_next else None
    prev_url = url_for(
        'admin.events_review',
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


@bp.route('/events/<int:id>/delete')
def events_delete(id):
    event = UpdateEvents.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event {id} has been deleted.')
    return redirect(url_for('admin.events_review'))


@bp.route('/events/<id>/allow')
def events_allow(id):
    event = UpdateEvents.query.get_or_404(id)
    event.allowed_status = True
    db.session.add(event)
    db.session.commit()
    flash(f'Event {id} has been approved.')
    return redirect(url_for('admin.events_review'))

# STUDENT STORIES

# Flask


@bp.route('/student-stories/review')
@login_required
def student_stories_review():
    flask_page = request.args.get('page', 1, type=int)
    ds_page = request.args.get('page', 1, type=int)

    # Flask
    flask_students = FlaskStudentStories.query.order_by(
        FlaskStudentStories.timestamp.desc()
        ).paginate(
            flask_page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.student_stories_review',
        flask_page=flask_students.next_num,
        _anchor="student-stories") \
        if flask_students.has_next else None
    prev_url = url_for(
        'admin.student_stories_review',
        flask_page=flask_students.prev_num,
        _anchor="student-stories") \
        if flask_students.has_prev else None
    all_flask_students = len(FlaskStudentStories.query.all())

    # Data Science
    ds_students = DataScienceStudentStories.query.order_by(
        DataScienceStudentStories.timestamp.desc()
        ).paginate(
            ds_page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_ds_url = url_for(
        'admin.data_science_review',
        ds_page=ds_students.next_num,
        _anchor="data-science") \
        if ds_students.has_next else None
    prev_ds_url = url_for(
        'admin.data_science_review',
        ds_page=ds_students.prev_num,
        _anchor="data-science") \
        if ds_students.has_prev else None
    all_ds_students = len(DataScienceStudentStories.query.all())
    return render_template(
        'admin/review_student_stories.html',
        title='Student Stories Review',
        flask_students=flask_students.items,
        ds_students=ds_students.items,
        next_url=next_url,
        prev_url=prev_url,
        next_ds_url=next_ds_url,
        prev_ds_url=prev_ds_url,
        all_flask_students=all_flask_students,
        all_ds_students=all_ds_students
        )


@bp.route('/student-stories/flask/<int:id>/delete')
def flask_stories_delete(id):
    student = FlaskStudentStories.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Flask story {id} has been deleted.')
    return redirect(url_for(
        'admin.student_stories_review',
        _anchor="student-stories"
        )
    )


@bp.route('/student-stories/flask/<id>/allow')
def flask_stories_allow(id):
    student = FlaskStudentStories.query.get_or_404(id)
    student.allowed_status = True
    db.session.add(student)
    db.session.commit()
    flash(f'Flask story {id} has been approved.')
    return redirect(url_for(
        'admin.student_stories_review',
        _anchor="student-stories"
        )
    )


@bp.route('/student-stories/data-science/<int:id>/delete')
def ds_stories_delete(id):
    student = DataScienceStudentStories.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Data Science story {id} has been deleted.')
    return redirect(url_for(
        'admin.student_stories_review',
        _anchor="student-stories"
        )
    )


@bp.route('/student-stories/data-science/<id>/allow')
def ds_stories_allow(id):
    student = DataScienceStudentStories.query.get_or_404(id)
    student.allowed_status = True
    db.session.add(student)
    db.session.commit()
    flash(f'Data Science story {id} has been approved.')
    return redirect(url_for(
        'admin.student_stories_review',
        _anchor="student-stories"
        )
    )

# Courses


@bp.route('/courses/update', methods=['GET', 'POST'])
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
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        course_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
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
        return redirect(url_for('admin.courses_update'))
    return render_template(
        'admin/update_courses.html',
        title='Courses Update',
        form=form
        )


@bp.route('/courses/review')
@login_required
def courses_review():
    page = request.args.get('page', 1, type=int)
    courses = UpdateCourses.query.order_by(
        UpdateCourses.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.courses_review',
        page=courses.next_num,
        _anchor="courses") \
        if courses.has_next else None
    prev_url = url_for(
        'admin.courses_review',
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


@bp.route('/courses/<int:id>/delete')
def courses_delete(id):
    course = UpdateCourses.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash(f'Course {id} has been deleted.')
    return redirect(url_for('admin.courses_review'))


@bp.route('/courses/<id>/allow')
def courses_allow(id):
    course = UpdateCourses.query.get_or_404(id)
    course.allowed_status = True
    db.session.add(course)
    db.session.commit()
    flash(f'Course {id} has been approved.')
    return redirect(url_for('admin.courses_review'))

# =================================
# END OF BLOG MANAGEMENT ROUTES
# =================================
