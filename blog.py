from app import app, db
from app.models import User, AnonymousTemplateInheritanceComment, Admin


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Admin=Admin,
        AnonymousTemplateInheritanceComment=AnonymousTemplateInheritanceComment
        )
