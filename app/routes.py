from app import app
from flask import render_template


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


@app.route('/blog/template-inheritance')
def blog_template_inheritance():
    return render_template(
        'blogs/template_inheritance.html',
        title='Template Inheritance'
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
