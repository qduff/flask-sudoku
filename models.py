
from flask_login import UserMixin

#from db import getuserinfo


class User(UserMixin):
    """Wraps User object for Flask-Login"""

    def __init__(self, dict):
        self.dict = dict
        self.id = dict

    def is_guest(self):
        if 'guest' in self.dict:
            if self.dict['guest'] == True:
                return True
            else:
                return False
        else:
            return False

    def get_id(self):
        return self.id

    def get_all(self):
        return self.id

    def is_active():
        return True

    def is_anonymous():
        return False

    def is_authenticated():
        return True
