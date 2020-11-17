from tinydb import TinyDB
from tinydb.queries import where

def open_db(func):
    db = TinyDB('users.json')
    def open_db_wrapper(*args, **kwargs):
        a = func(db,*args, **kwargs)
        db.close()
        return a
    return open_db_wrapper
    
@open_db
def dothing(db):
    return len(db)

print(dothing())

#userrow = userdb.search(where('username') == 'ds')
#
#if userrow:
#    print(userrow)
#else:
#    print('jdhsdf')

