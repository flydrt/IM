from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio
from forms import User
from views import roomMap


# @socketio.on('message')
# def chat_message(message):
#     emit('message', {'data': message['data'], 'from': message['from'], 'to': message['to']}, broadcast = True)


@socketio.on('join')
def on_join():
    if current_user.id in roomMap:
        room = roomMap[current_user.id]
        join_room(room)


@socketio.on('leave')
def on_leave():
    leave_room(roomMap[current_user.id])


@socketio.on('message')
def chat_message(message):
    emit('message', {'data': message['data'], 'from': message['from'], 'to': message['to']}, room=roomMap[current_user.id])