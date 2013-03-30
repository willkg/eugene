# Holds settings for the test environment
from eugene.settings import *

TESTING = True

# This looks wrong, but it's an in-memory sqlite3 db
# for faster testing.
DATABASE_URL = 'sqlite://'
