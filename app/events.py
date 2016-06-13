from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio
from models import User, Message
from views import roomMap
from app import db


@socketio.on('join')
def on_join(message):
    if current_user.id in roomMap:
        room = roomMap[current_user.id]
        join_room(room)

        to_id = User.query.filter_by(username=message['to']).first().id
        for msg in Message.query.filter_by(to_id=current_user.id).all():
            if msg.status is False and msg.from_id == to_id:
                msg.status = True
                db.session.add(msg)
                db.session.commit()
                emit('message', {'data': msg.message, 'from': message['to'], 'to': message['from'], 'flag': 0}, room=room)


@socketio.on('leave')
def on_leave():
    leave_room(roomMap[current_user.id])
    del roomMap[current_user.id]


@socketio.on('message')
def chat_message(message):
    user = User.query.filter_by(username=message['from']).first()
    friend = User.query.filter_by(username=message['to']).first()
    msg = Message(from_id=user.id, to_id=friend.id, message=message['data'], status=0)

    room = roomMap[current_user.id]
    for key in roomMap:
        if roomMap[key] == room and key != user.id:
            msg.status = True

    db.session.add(msg)
    db.session.commit()
    emit('message', {'data': message['data'], 'from': message['from'], 'to': message['to'], 'flag': 1}, room=room)