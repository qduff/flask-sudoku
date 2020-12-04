#from addict import Dict
from datetime import timedelta
import random

games = {}
#games = Dict()


def addGame(roomname: str, gametype: str, password: str = None, playersrequired: int = 2, autoclear:bool = True, difficulty:str = 'medium') -> str:
    codelen = 4
    roomcode = 0
    while roomcode == 0 or roomcode in games:
        roomcode = ''.join(["{}".format(random.randint(1, 9)) for _ in range(0, codelen)])
    games.update(
        {roomcode:
            {'name': roomname,
             'autoclear': autoclear,
             'gametype': gametype,
             'password': password,
             'started': False,
             'timestarted': None,
             'playersrequired': playersrequired,
             'players': {},
             'numcompleted': 0,
             'difficulty': difficulty
             }
         }
    )
    return roomcode


def addUser(username: str, roomcode: str, role: str = 'default'):
    games[roomcode]['players'].update(
        {username:
            {'role': role,
             'completed': False,
             'timecompleted': None,
             'timetaken': None,
             'place': None,
             'latestsubmit':None
             }
         }
    )


def removeGame(roomcode: str):
    games.pop(roomcode)


def removeUser(username: str, roomcode: str):  # Do the admining other player heres
    games[roomcode]['players'].pop(username)


def setRole(username: str, roomcode: str, role: str):
    setUserProperty(roomcode, username, 'role', role)


def setGameProperty(roomcode, property, desired):
    games[roomcode][property] = desired


def setUserProperty(roomcode, username, property, desired):
    games[roomcode]['players'][username][property] = desired

# GET

def getUserCompletionTime(roomcode,username):
    return round(getUserProperty(roomcode,username,'timetaken').total_seconds(),1)
    

def getGameProperty(roomcode, property):
    return games[roomcode][property]


def getUserProperty(roomcode,username, property):
    return games[roomcode]['players'][username][property]


def gameExists(roomcode) -> bool:
    if roomcode in games:
        return True
    else:
        return False
  
  
def getPlayers(roomcode:str):
    return getGameProperty(roomcode,'players')


def playerExists(username:str, roomcode:str) -> bool:
    if username in getPlayers(roomcode): return True
    else: return False
    

def playerRole(username:str, roomcode:str) -> str:
    return getUserProperty(roomcode,username,'role')


def playerCount(roomcode:int) -> int:
    return len(getPlayers(roomcode))

