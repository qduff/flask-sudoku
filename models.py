
from flask_login import UserMixin

#from db import getuserinfo

class User(UserMixin):
    """Wraps User object for Flask-Login"""
    def __init__(self, dict):
        self.dict = dict
        print('DISTFSDK:JJGSKLJGKSL',dict)
        self.id = dict

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
    
    
