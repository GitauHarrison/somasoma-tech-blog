from app import app, db
from app.models import User, AnonymousTemplateInheritanceComment, Admin,\
    UpdateBlog, UpdateEvents, UpdateCourses, FlaskStudentStories


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Admin=Admin,
        UpdateBlog=UpdateBlog,
        UpdateEvents=UpdateEvents,
        UpdateCourses=UpdateCourses,
        FlaskStudentStories=FlaskStudentStories,
        AnonymousTemplateInheritanceComment=AnonymousTemplateInheritanceComment
        )
