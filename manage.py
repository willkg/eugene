#!/usr/bin/env python
import os

from flask.ext.script import Manager

from eugene.wsgi import app


manager = Manager(app)
app_path = os.path.join(os.path.dirname(__file__), 'eugene')


if __name__ == '__main__':
    manager.run()
