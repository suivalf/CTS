from app import app
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Coin': Coin}