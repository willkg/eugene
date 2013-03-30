import os

from eugene.helpers import truthiness

DEBUG = truthiness(os.environ.get('DEBUG', False))
DATABASE_URL = os.environ.get('DATABASE_URL')
BLUEPRINTS = [
    'eugene.comms'
]

TESTING = False

try:
    from settings_local import *
except ImportError:
    pass
