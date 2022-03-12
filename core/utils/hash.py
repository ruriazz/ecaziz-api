from hashids import Hashids
from core.variables import app_config

class Hash:

    class UserId(object):
        def __init__(self):
            self.hashids = Hashids(salt=app_config.get('salt_user'))

        def encode(self, value : int):
            try:
                return self.hashids.encrypt(value)
            
            except:
                return False

        def decode(self, value : str):
            try:
                return self.hashids.decrypt(value)

            except:
                return False