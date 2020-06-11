from app import app, db, cli
from app.models import User, Comments

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Comments': Comments, 'User': User}