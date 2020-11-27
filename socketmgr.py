from os import name
from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit, rooms
from flask_login import current_user
from gamesdb import games
from flask.helpers import url_for
import datetime
from sudokutools.generate import generate

app = create_app()

socketio = SocketIO(app)

user_to_sid = {}
sid_to_user = {}

###############################################
#################    LOBBY   ##################
###############################################

#@socketio.on('getusers')
#def handle_my_custom_event(json):
#    socketio.emit('my response', json)
    

@socketio.on('join')
def on_join(data):
    username = current_user.dict['username']
    room = data['room']
    
    if int(room) in games:
        join_room(room)
        
        
        print(f'{username} has joined the room')
        if int(room) in games:
            userdict = genuserdict(room)
            emit('userupdate', userdict, room=room, json=True)
        else:
            return False


@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    room = data['room']
    print('leave event triggered by '+username)
    leave_room(room)

    if int(room) in games:
        if username in games[int(room)]['players']:
            if games[int(room)]['players'][current_user.dict['username']]['admin'] == True:
                if len(games[int(room)]['players']) >= 2:
                    print('move admin to antoher player')
                    for username  in games[int(room)]['players']:
                        print(games[int(room)]['players'][username]['admin'])
                        if games[int(room)]['players'][username]['admin'] == False:
                            games[int(room)]['players'][username]['admin'] = True
            print(f"popping {current_user.dict['username']}")
            games[int(room)]['players'].pop(current_user.dict['username'])        
        if len(games[int(room)]['players']) == 0:
            games.pop(int(room))
        if int(room) in games and len(games[int(room)]['players']) != 0:
            userdict = genuserdict(room)
            emit('userupdate',userdict, room=room, json=True)
        else:
            return False
        send(username + ' has left the room.', room=room)
    
@socketio.on('requestgamestart')
def onrequestgamestart(data):
    username = current_user.dict['username']
    room = data['room']
    print('starrt event triggered by '+username)
    if int(room) in games:
        nplayers = len(games[int(room)]['players'])
        if nplayers >=2:
            if games[int(room)]['players'][username]['admin'] == True:
                print('you may start!, sending start')
                url = str(url_for('game.playpage', id=room))
                json = {'url':url}
                json['players'] = genuserdict(room)
                games[int(room)]['started'] = True
                
                sudoku, solution = generate()
                #GEN SUDOKU
                games[int(room)]['sudoku'] = sudoku
                games[int(room)]['sudokusol'] = solution


                emit('startgame',json, room=room, json=True)
            else: return emit('cannotstart',{'msg':f'You are not an admin.'}, json=True)
        else: emit('cannotstart',{'msg':f"At least {games[int(room)]['playersrequired']} Players required to start, only {nplayers} in the lobby."}, json=True)

      
###############################################
#################    GAME   ###################
############################################### 
      

@socketio.on('requestsudoku')
def onrequestgamestart(data):
    username = current_user.dict['username']
    room = data['room']
    

    if room == "":
        return

    if int(room) in games:
        
        join_room(room)

        
        if games[int(room)]['players'][username]['timestarted'] == None:
            games[int(
                room)]['players'][username]['timestarted'] = datetime.datetime.now()

        sudokustring = games[int(room)]['sudoku']

        if games[int(room)]['players'][username]['completed'] == False:
            emit('sudokustr', {'content': sudokustring}, json=True)
        else:
            # Covers refresh case
            time = games[int(room)]['players'][username]['completed']
            emit('completed', {'time': f"{time.total_seconds()}"}, json=True)
    else:
        emit('redirect', {'url': f"/"}, json=True)


@socketio.on('submitsudoku')
def sudokusubmit(data):
    username = current_user.dict['username']
    room = data['room']

    if room == "": 
        return
    
    #check that user has not already completed the sudoku (done), and started
    if games[int(room)]['players'][username]['completed'] == False:  # does this even work? apparently. 
        if int(games[int(room)]['sudokusol']) == int(data['string']):
            time = datetime.datetime.now() - games[int(room)]['players'][username]['timestarted']
            games[int(room)]['players'][username]['completed'] = time
            
            emit('completed', {'time': f"{time.total_seconds()}"} ,json=True)
            
            #ALSO send to room!
            
            

            print('sent')
            #broadcast completion!
        
        completiondict = gencompletiondict(room=room) # send complete table, regardless of correctness
        emit('tableupdate', completiondict, json=True, room=room)
            
            
    else: # If already done (shouldnt happen)
        emit('completed',{'time':f"{games[int(room)]['players'][username]['completed'].total_seconds()}"}, json=True)


def gencompletiondict(room):
    completiondict = {}
    for item in games[int(room)]['players']:
        if games[int(room)]['players'][item]['admin'] == True:
            role = 'admin'
        else:
            role = 'default'
        
        if games[int(room)]['players'][item]['completed'] == False:
            completed = 'false'
        else:
            completed = str(games[int(room)]['players'][item]['completed'].total_seconds())

        completiondict[str(item)] = {'role':str(role), 'completed':completed}


    return completiondict


def genuserdict(room):
    userdict = {}
    for item in games[int(room)]['players']:
        if games[int(room)]['players'][item]['admin'] == True:
            role = 'admin'
        else:
            role = 'default'
        userdict.update({str(item): str(role)})
    return userdict
