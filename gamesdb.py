#from addict import Dict
games = {}
#games = Dict()


def addGame(roomcode:str, type:str):
    pass

def addUser(username:str, roomcode:str):
    pass


def removeGame(roomcode:str):
    games.pop(roomcode)

def removeUser(username:str, roomcode:str): # Do the admining other player heres
    games[roomcode]['players'].pop(username)      



def setRole(username:str, roomcode:str, role:str):
    games[roomcode]['players'][username]['admin'] = role
    
    
def setGameProperty(roomcode, property, desired):
    pass

def setUserProperty(roomcode, property, desired):
    pass

def getGameProperty(roomcode, property):
    pass

def getUserProperty(roomcode, property):
    pass


def gameExists(roomcode) -> bool:
    if roomcode in games:
        return True
    else:
        return False
 
        
def getPlayers(roomcode:str):
    return games[roomcode]['players']

def playerExists(username:str, roomcode:str) -> bool:
    if username in games[roomcode]['players']:
        return True
    else:
        return False

def playerRole(username:str, roomcode:str) -> str:
    return games[roomcode]['players'][username]['role']


def playerCount(roomcode:int) -> int:
    return len(games[roomcode]['players'])