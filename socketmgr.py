from os import name
from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit, rooms
from flask_login import current_user
from gamesdb import *
from flask.helpers import url_for
import datetime
from sudokutools.generate import generate

app = create_app()

socketio = SocketIO(app)

###############################################
#################    LOBBY   ##################
###############################################

#@socketio.on('getusers')
#def handle_my_custom_event(json):
#    socketio.emit('my response', json)
    

@socketio.on('join')
def on_join(data):
    username = current_user.dict['username']
    roomcode = data['room']
    
    if gameExists(roomcode):
        join_room(roomcode)
        emit('userupdate', lobbydict(roomcode), room=roomcode, json=True)


@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    roomcode = data['room']
    
    leave_room(roomcode)
    if gameExists(roomcode) and playerExists(username, roomcode):
        if playerCount(roomcode) >= 2:
            if playerRole(username, roomcode) == 'admin':
                for tempuser in getPlayers(roomcode):
                    madeadmin = False
                    if playerRole(tempuser, roomcode) != 'admin' and madeadmin == False:
                        setRole(tempuser, roomcode, 'admin')
                        madeadmin = True
        
            emit('userupdate', lobbydict(roomcode), room=roomcode, json=True)
            removeUser(username, roomcode)
        else:
            removeGame(roomcode)


@socketio.on('requestgamestart')    #make this nice next
def onrequestgamestart(data):
    username = current_user.dict['username']
    roomcode = data['room']
    
    #print('starrt event triggered by '+username)
    if gameExists(roomcode):
        nplayers = playerCount(roomcode)
        if nplayers >=2:
            if playerRole(username, roomcode) == 'admin':
                json = {'url': str(url_for('game.playpage', roomcode=roomcode)),
                        'players':lobbydict(roomcode)}
                
                sudoku,sudokusol  = generate(getGameProperty(roomcode,'difficulty')) # TODO Automate this 

                setGameProperty(roomcode,'sudoku',sudoku)
                setGameProperty(roomcode,'sudokusol', sudokusol) 

                setGameProperty(roomcode,'started',True)

                setGameProperty(roomcode,'timestarted', datetime.datetime.now())

                emit('startgame',json, room=roomcode, json=True)
            else: emit('cannotstart',{'msg':f'You are not an admin.'}, json=True)
        else: emit('cannotstart',{'msg':f"At least {getGameProperty(roomcode,'playersrequired')} Players required to start, only {nplayers} in the lobby."}, json=True)

      
###############################################
#################    GAME   ###################
############################################### 
      

@socketio.on('requestsudoku')
def onrequestgamestart(data):
    username = current_user.dict['username']
    roomcode = data['room']


    if roomcode == "":
        return
    
    if gameExists(roomcode) and getGameProperty(roomcode, 'started') == True:
        join_room(roomcode)

        #if games[roomcode]['players'][username]['timestarted'] == None:
        #    games[roomcode]['players'][username]['timestarted'] = datetime.datetime.now()

        if getUserProperty(roomcode,username,'completed') == False:
            emit('sudokustr', {'sudoku': getGameProperty(roomcode,'sudoku'), 'autoclear': getGameProperty(roomcode,'autoclear')}, json=True)
        else:  # Covers refresh case
            emit('completed', getcompletedjson(roomcode, username), json=True)

        # send complete table, so the player has a table (DOES _NOT_ have to be to room but might as well)
        emit('tableupdate', completiontabledict(roomcode=roomcode), json=True, room=roomcode)

    else:  # Does nothing on client side, futureproofing, i guess
        emit('redirect', {'url': f"/"}, json=True)


@socketio.on('submitsudoku')
def sudokusubmit(data):
    username = current_user.dict['username']
    roomcode = data['room']
    
    if roomcode == "": 
        return
    
    #check that user has not already completed the sudoku (done), and started
    if getUserProperty(roomcode,username,'completed') == False:  # does this even work? apparently.
        setUserProperty(roomcode,username, 'latestsubmit', data['string'])
        
        if getGameProperty(roomcode,'sudokusol') == data['string'] or 'complete' in data:  #DEBUG DEBUG    
            currenttime = datetime.datetime.now()
            setUserProperty(roomcode,username,'timecompleted',desired=currenttime)
            timetaken = currenttime - getGameProperty(roomcode,'timestarted')
            setUserProperty(roomcode,username,'timetaken',desired=timetaken) 
            setUserProperty(roomcode,username,'completed',True)
            
            newnumcompleted =  getGameProperty(roomcode,'numcompleted')+1
            setGameProperty(roomcode,'numcompleted', newnumcompleted) 
            
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            setUserProperty(roomcode,username,'place', ordinal(newnumcompleted))
            
            emit('completed', getcompletedjson(roomcode,username) ,json=True)

        # send complete table, regardless of correctness
        emit('tableupdate',completiontabledict(roomcode) , json=True, room=roomcode)
            
    else: # If already done (shouldnt happen)
        emit('completed', getcompletedjson(roomcode,username) ,json=True)



def getcompletedjson(roomcode,username):
    place = getUserProperty(roomcode,username,'place')
    time = getUserCompletionTime(roomcode,username)
    return {'place':f'You came in {place} Place!','time': f"Completed in {time}s!"}


def completiontabledict(roomcode):  # do progress also, and order by completion
    totalnums = len(getGameProperty(roomcode, 'sudokusol'))
    nonzeronums = len(str(getGameProperty(roomcode, 'sudoku')).replace('0',''))
    numempty = totalnums - nonzeronums
    
    completiondict = {'empty': numempty, 'players':{}}
    
    for username in getPlayers(roomcode):
        if playerRole(username, roomcode) == 'admin':
            role = 'admin'
        else:
            role = 'default'
            
        if getUserProperty(roomcode, username, 'completed') == False:
            completed = 'false'
        else:
            completed = str(getUserCompletionTime(roomcode,username))+'s'
        
        latestsubmit = getUserProperty(roomcode, username, 'latestsubmit')
                
        if latestsubmit == None:
            filledlen = 0
        else:
            latestsubmit = str(latestsubmit).replace('0','')
            filledlen = numempty - ( totalnums - len(latestsubmit)) # works?
        
        place = getUserProperty(roomcode, username, 'place')

        completiondict['players'][username] = {'role':role, 'completed':completed, 'filledlen':filledlen, 'place':place}
        
    return completiondict


def lobbydict(room):
    userdict = {}
    for item in games[room]['players']:
        if playerRole(item, room) == 'admin':
            role = 'admin'
        else:
            role = 'default'
        userdict.update({str(item): str(role)})
    return userdict
