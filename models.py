
from flask_login import UserMixin

#from db import getuserinfo

class User(UserMixin):
    """Wraps User object for Flask-Login"""
    def __init__(self, dict):

            
        self._called = True

        
        
        self.dict = dict
        print('DISTFSDK:JJGSKLJGKSL',dict)
        self.id = dict

    def is_guest(self):
        try:
            if self.dict['guest']:
                return True
        except:
            return False

    def get_id(self):
        return self.id 

    def get_all(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    
