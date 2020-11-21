from flask.globals import current_app
from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_login import current_user

from games import games

import logging

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = create_app()
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('getusers')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json)+' from '+current_user.dict['username'])
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('join')
def on_join(data):
    username = current_user.dict['username']
    room = data['room']
    join_room(room)
    print(username + f' has entered the room. {room}{type(room)}')
    try:
        print(games)
        for item in games[int(room)]['players']:
            print(item)
            
        emit('userupdate',  {'users':{'quentin':'admin','fds':'default'}}, room=room, json=True)
    except:
        pass
    #send(username + ' has entered the room.', room=room) #MAKE WODK


@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
    
def ctxsend(*args, **kwargs):
    send(*args,**kwargs)

if __name__ == "__main__":
    print('\n\n\nRunning\n-----------------')
    socketio.run(app, host='0.0.0.0', port=8001)