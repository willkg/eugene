import json
import time

from nose.tools import eq_

from eugene.comms.models import User, Message
from eugene.comms.tests import user
from eugene.database import get_session
from eugene.tests import BaseTestCase, load_json


class TestMessages(BaseTestCase):
    def test_post_message(self):
        data = json.dumps({
                'sender': 'SHIP1',
                'recipient': 'SHIP2',
                'text': 'HAIL'
        })

        response = self.client.post('/api/v1/message', data=data,
                                    content_type='application/json')

        eq_(response.status_code, 200)
        eq_(response.data, '{"status": "ok"}')

        db = get_session(self.app)
        messages = db.query(Message).all()
        eq_(len(messages), 1)

    def test_post_message_to_everyone(self):
        db = get_session(self.app)

        ship1 = user(name='ship1')
        db.add(ship1)
        ship2 = user(name='ship2')
        db.add(ship2)
        ship3 = user(name='ship3')
        db.add(ship3)
        db.commit()

        data = json.dumps({
                'sender': 'SHIP1',
                'recipient': 'EVERYONE',
                'text': 'HAIL'
        })

        response = self.client.post('/api/v1/message', data=data,
                                    content_type='application/json')

        eq_(response.status_code, 200)
        eq_(response.data, '{"status": "ok"}')

        messages = db.query(Message).all()
        eq_(len(messages), 3)

    def test_get_message(self):
        db = get_session(self.app)
        msg1 = Message(sender='ship1', recipient='ship2', text='hail!')
        db.add(msg1)
        db.commit()

        response = self.client.get('/api/v1/message/ship2')

        eq_(response.status_code, 200)
        msgs = load_json(response.data)
        eq_(len(msgs['messages']), 1)

    def test_get_message_none_for_me(self):
        db = get_session(self.app)
        msg1 = Message(sender='ship1', recipient='ship2', text='hail!')
        db.add(msg1)
        db.commit()

        response = self.client.get('/api/v1/message/ship1')

        eq_(response.status_code, 200)
        msgs = load_json(response.data)
        eq_(len(msgs['messages']), 0)

    def test_get_message_none_recent(self):
        db = get_session(self.app)
        msg1 = Message(sender='ship1', recipient='ship2', text='hail!',
                       created=time.time() - (120 * 5))
        db.add(msg1)
        db.commit()

        response = self.client.get('/api/v1/message/ship2')

        eq_(response.status_code, 200)
        msgs = load_json(response.data)
        eq_(len(msgs['messages']), 0)


class TestUser(BaseTestCase):
    def test_user_none(self):
        db = get_session(self.app)
        ships = db.query(User).all()
        eq_(len(ships), 0)
        response = self.client.get('/api/v1/user')
        data = load_json(response.data)
        eq_(len(data['users']), 0)

    def test_user_one(self):
        db = get_session(self.app)
        data = json.dumps({'available': True})
        response = self.client.post('/api/v1/user/ship1', data=data,
                                    content_type='application/json')
        eq_(response.data, '{"status": "ok"}')

        ships = db.query(User).all()
        eq_(len(ships), 1)
        response = self.client.get('/api/v1/user')
        data = load_json(response.data)
        eq_(len(data['users']), 1)

    def test_user_unuser(self):
        db = get_session(self.app)
        data = json.dumps({'available': True})
        response = self.client.post('/api/v1/user/ship1', data=data,
                                    content_type='application/json')
        eq_(response.data, '{"status": "ok"}')

        data = json.dumps({'available': False})
        response = self.client.post('/api/v1/user/ship1', data=data,
                                    content_type='application/json')
        eq_(response.data, '{"status": "ok"}')

        ships = db.query(User).all()
        eq_(len(ships), 0)
        response = self.client.get('/api/v1/user')
        data = load_json(response.data)
        eq_(len(data['users']), 0)
