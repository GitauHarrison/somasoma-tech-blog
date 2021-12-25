from app import create_app, db
from app.models import User, AnonymousTemplateInheritanceComment, Admin,\
    UpdateBlog, UpdateEvents, UpdateCourses, FlaskStudentStories,\
    DataScienceStudentStories

app = create_app()


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
        DataScienceStudentStories=DataScienceStudentStories,
        AnonymousTemplateInheritanceComment=AnonymousTemplateInheritanceComment
        )
