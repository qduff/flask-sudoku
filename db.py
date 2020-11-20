from tinydb import TinyDB
from tinydb.queries import where

def open_db(func):
    db = TinyDB('users.json')
    def open_db_wrapper(*args, **kwargs):
        a = func(db,*args, **kwargs)
        db.close()
        return a
    return open_db_wrapper

 #userdb.insert({'username':'quentin','password':generate_password_hash('test','sha256')})