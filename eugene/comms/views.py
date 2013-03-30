import time

from flask import Blueprint, current_app, render_template, request

from eugene.comms.models import User, Message
from eugene.database import get_session
from eugene.helpers import jsonify


blueprint = Blueprint('comms', __name__,
                      template_folder='templates')


def update_status(name):
    db = get_session(current_app)

    user = db.query(User).filter_by(name=name).first()
    if not user:
        user = User(name=name)
        db.add(user)
    user.updated = int(time.time())
    db.commit()


@blueprint.route('/')
def index():
    return render_template('comms/index.html')


@blueprint.route('/api/v1/message', methods=['POST'])
def post_message():
    sender = request.json.get('sender').upper()
    recipient = request.json.get('recipient').upper()
    text = request.json.get('text')

    db = get_session(current_app)

    update_status(sender)

    if recipient == 'EVERYONE':
        recipients = db.query(User).all()
        for recipient in recipients:
            msg = Message(sender, recipient.name, text)
            db.add(msg)

    else:
        msg = Message(sender, recipient, text)
        db.add(msg)

    db.commit()

    return jsonify({'status': 'ok'})


@blueprint.route('/api/v1/message/<name>', methods=['GET'])
def get_message(name):
    name = name.upper()

    db = get_session(current_app)
    start_time = time.time() - (60 * 5)
    msgs = (db.query(Message)
            .filter(Message.created >= start_time)
            .filter(Message.recipient == name))

    msgs = [[msg.id, msg.sender, msg.text, msg.created]
            for msg in msgs]

    update_status(name)
    db.commit()

    return jsonify({
            'status': 'ok',
            'messages': msgs
    })


@blueprint.route('/api/v1/user/<name>', methods=['POST'])
def update_user(name):
    name = name.upper()
    available = request.json.get('available')

    db = get_session(current_app)

    ship = db.query(User).filter_by(name=name).first()
    if not available:
        if ship:
            db.delete(ship)

    else:
        if not ship:
            ship = User(name)
            db.add(ship)
        ship.available()

    db.commit()
    return jsonify({'status': 'ok'})


@blueprint.route('/api/v1/user', methods=['GET'])
def get_users():
    db = get_session(current_app)

    start_time = time.time() - (60 * 5)
    users = (db.query(User)
            .filter(User.updated >= start_time))
    users = [av.name for av in users]

    return jsonify({
            'status': 'ok',
            'users': users
    })
