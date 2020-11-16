from tinydb import TinyDB, Query

from werkzeug.security import generate_password_hash, check_password_hash


userdb = TinyDB('users.json')

#userdb.insert({'username':'quentin','password':generate_password_hash('test','sha256')})


userrow = userdb.search(Query().username == 'ds')

if userrow:
    print(userrow)
else:
    print('jdhsdf')

