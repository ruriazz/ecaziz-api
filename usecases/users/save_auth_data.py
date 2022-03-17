from django.contrib.auth.hashers import make_password

from applications.users.models import AuthenticatedUser,User

# TODO: usecases.users.save_auth_data
def save_auth_data(user : User, new_token : str, old_token : str = None):
    if old_token:
        auth = AuthenticatedUser()
    else:
        auth = AuthenticatedUser()
        auth.token = make_password(new_token)
        auth.user = user
        
        auth.save()