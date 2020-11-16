
from flask_login import UserMixin
from db import getuserinfo
class User(UserMixin):
    """Wraps User object for Flask-Login"""
    def __init__(self, id):
        self.id = id
        
    def get_id(self):
        return self.id 
    
    def get_all(self):
        return self.id

    def is_active(self):
        print('test')
        return getuserinfo(self.get_id())['enabled']

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def get_key(self, key):
        return getuserinfo(self.get_id())[key]
    #get key directy instead of al 
    
    
    
