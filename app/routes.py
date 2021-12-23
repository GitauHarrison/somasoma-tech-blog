from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import AnonymousCommentForm
from app.models import AnonymousTemplateInheritanceComment, User


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
