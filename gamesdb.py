#from addict import Dict
from datetime import timedelta


games = {}
#games = Dict()


#SET

def addGame(roomcode:str, type:str):
    pass


def addUser(username:str, roomcode:str, role:str = 'default'):
    games[roomcode]['players'].update(
        {username:
            {'role': role,
             'completed':False,
             'timestarted':None,
             'timecompleted':None,
             'timetaken':None
             }
        }
    )



def removeGame(roomcode:str):
    games.pop(roomcode)

def removeUser(username:str, roomcode:str): # Do the admining other player heres
    games[roomcode]['players'].pop(username)      


def setRole(username:str, roomcode:str, role:str):
    setUserProperty(roomcode,username,'role',role)

    
def setGameProperty(roomcode, property, desired):
    games[roomcode][property] = desired

def setUserProperty(roomcode,username, property, desired):
    games[roomcode]['players'][username][property] = desired

#GET

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