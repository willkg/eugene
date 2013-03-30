import os

from eugene.helpers import truthiness

DEBUG = truthiness(os.environ.get('DEBUG', False))
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///eugene_app.db')
BLUEPRINTS = [
    'eugene.comms'
]

TESTING = False

try:
    from settings_local import *
except ImportError:
    pass
