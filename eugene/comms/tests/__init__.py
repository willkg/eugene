import datetime
import time

from eugene.comms.models import User, Message


def user(**kwargs):
    """Model maker for User"""
    return User(**kwargs)


def message(**kwargs):
    """Model maker for Message"""
    defaults = {
        'message_type': 0,
        'sender': 'SHIP1',
        'recipient': 'SHIP2',
        'text': 'HAIL.',
        'created': int(time.time()),
        }

    if 'created' in kwargs:
        created = kwargs['created']
        if isinstance(created, datetime.datetime):
            created = int(time.mktime(created.time_tuple()))
        kwargs['created'] = created

    defaults.update(kwargs)

    return Message(**defaults)
