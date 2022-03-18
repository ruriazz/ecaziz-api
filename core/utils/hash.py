import datetime, jwt, hashlib
from django.contrib.auth.hashers import make_password, check_password
from hashids import Hashids
from applications.users.models import AuthenticatedUser, User
from core.variables import app_config

class Hash:
    def encode(hashids:Hashids, value:int):
        try:
            return hashids.encrypt(value)
        
        except:
            return False

    def decode(hashids:Hashids, value:str):
        try:
            return hashids.decrypt(value)
        except:
            return False

    class UserId(object):
        def __init__(self):
            self.__hashids = Hashids(salt=app_config.get('salt_user'))

        def encode(self, value:int): return Hash.encode(self.__hashids, value)
        def decode(self, value:int): return Hash.decode(self.__hashids, value)

    class AuthId(object):
        def __init__(self):
            self.__hashids = Hashids(salt=app_config.get('salt_auth'))

        def encode(self, value:int): return Hash.encode(self.__hashids, value)
        def decode(self, value:int): return Hash.decode(self.__hashids, value)[0]

class JWT(object):

    def __init__(self):
        self.__secret_key = app_config.get('secret_key')
        self.__algorithm = 'HS256'
        self.__iss = "ruriazz.warkopwarawiri.id"
        self.__aud = "ruriazz.warkopwarawiri.id"

    def encode(self, payload:dict, headers:dict = {}):
        return jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm, headers = headers).decode('utf-8')

    def decode(self, token):
        
        try:
            decoded = jwt.decode(token, self.__secret_key, algorithm='HS256', audience=self.__aud, options={'verify_exp': False})
            headers = jwt.get_unverified_header(token)
            return {
                'headers': headers,
                'payload': decoded,
            }
        except:
            return False

    @staticmethod
    def build(user:User):
        if not user.id:
            return False

        inclass = JWT()

        auth = AuthenticatedUser()
        auth.user = user
        auth.token = "build"
        auth.save()

        token = inclass.encode(
            payload = {
                "iss": inclass.__iss,
                "aud": inclass.__aud,
                "iat": auth.authenticated_at,
                "exp": auth.authenticated_at + datetime.timedelta(minutes=30),
            },
            headers = {
                "kid": Hash.AuthId().encode(auth.id)
            }
        )
        
        auth.token = make_password(token)
        auth.save()

        return token

    @staticmethod
    def verify(token:str):
        inclass = JWT()

        decoded = inclass.decode(token)

    @staticmethod
    def refresh(token:str):
        inclass = JWT()

        decoded = inclass.decode(token)
        if not decoded:
            return False

        kid = decoded.get('headers').get('kid')
        iss = decoded.get('payload').get('iss')
        aud = decoded.get('payload').get('aud')
        now = datetime.datetime.now().timestamp()

        print("aud", aud)

        if iss != inclass.__iss:
            return False

        if aud != inclass.__aud:
            return False

        if not AuthenticatedUser.objects.filter(id=Hash.AuthId().decode(kid)).exists():
            return False

        auth = AuthenticatedUser.objects.get(id=Hash.AuthId().decode(kid))
        if not check_password(token, auth.token):
            return False

        if now < (auth.authenticated_at + datetime.timedelta(minutes=30)).timestamp():
            return token
        else:
            new_token = JWT.build(auth.user)
            auth.delete()

            return new_token

    @staticmethod
    def Payload(iss:str = None, aud:str = None, iat:datetime = None, exp:datetime = None, claims:dict = None):
        class DataPayload(object):
            def __init__(self, iss:str, aud:str, iat:datetime, exp:datetime, claims:dict = None):
                self.iss = iss
                self.aud = aud
                self.iat = iat
                self.exp = exp
                self.claims = claims

            def to_dict(self):
                return {
                    'iss': self.iss,
                    'aud': self.aud,
                    'iat': self.iat,
                    'exp': self.exp,
                    'claims': self.claims
                }

        return DataPayload(
            iss = iss,
            aud = aud,
            iat = iat,
            exp = exp,
            claims = claims
        )