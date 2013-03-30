import time

from eugene.database import Base
from sqlalchemy import Column, Integer, String, Sequence


MESSAGE_TYPES = {
    0: 'message'
    }


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, Sequence('message_id_seq'), primary_key=True,
                autoincrement=True)
    message_type = Column(Integer())
    sender = Column(String())
    recipient = Column(String())
    text = Column(String())
    created = Column(Integer())  # seconds since epoch

    def __init__(self, sender, recipient, text, created=None):
        self.sender = sender.upper()
        self.recipient = recipient.upper()
        self.text = text.upper()
        self.created = created or int(time.time())

    def __repr__(self):
        return '<Message {0}: {1}: {2}>'.format(
            self.id, self.recipients, self.text[:20])


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True,
                autoincrement=True)
    name = Column(String())
    updated = Column(Integer())  # seconds since epoch

    def __init__(self, name, updated=None):
        self.name = name.upper()
        self.updated = updated or int(time.time())

    def available(self):
        self.updated = int(time.time())
