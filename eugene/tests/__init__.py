import simplejson as json
import unittest
from collections import OrderedDict
from functools import wraps

from flask import current_app, Request
from werkzeug.test import create_environ

from eugene import settings_test
from eugene.database import get_session, Base
from eugene.main import create_app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app = create_app(settings_test)
        self.client = self.app.test_client()
        for app in self.app.blueprints:
            try:
                __import__('%s.models' % app)
            except ImportError:
                pass
        db = get_session(self.app)
        Base.metadata.create_all(db.bind)

    def tearDown(self):
        db = get_session(self.app)
        Base.metadata.drop_all(db.bind)
        db.close()


def load_json(s):
    """Loads JSON to an ordered dict"""
    return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(s)


def create_request(*args, **kwargs):
    """Creates a test request object"""
    env = create_environ(*args, **kwargs)
    return Request(env)
