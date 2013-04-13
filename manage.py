#!/usr/bin/env python
import os

from flask.ext.script import Manager

from eugene.comms.utils import export_log, InvalidFormat
from eugene.database import create_all
from eugene.wsgi import app


manager = Manager(app)
app_path = os.path.join(os.path.dirname(__file__), 'eugene')

db_repo = os.path.join(app_path, 'migrations')
db_url = app.config.get('DATABASE_URL')


@manager.command
def db_create():
    """Create the database"""
    create_all(app)
    print 'Database created: {0}'.format(app.config['DATABASE_URL'])


@manager.option('--output', help='Output format: html or csv', default='html')
def export(output):
    """Generates a log of the eugene data"""
    try:
        logname = export_log(output)
        print 'Exported log as {0}.'.format(logname)
    except InvalidFormat as exc:
        print 'Error: ' + exc.message


if __name__ == '__main__':
    manager.run()
