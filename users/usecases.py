# TODO: usecases.users

from ipaddress import ip_address
import time
from datetime import datetime, timezone
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from core.utils.handlers import get_client_ip, get_client_ua
from core.utils.response import ApiResponse

from .models import AuthenticatedUser, AuthenticationAttempt, User
from .serializers import UserSerializer

# TODO: usecases.users.user_authentication
def user_authentication(request):
    data = {
        'username': str(request.data.get('username')).strip(),
        'password': str(request.data.get('password'))
    }

    ip = get_client_ip(request)
    ua = get_client_ua(request)

    attempted = AuthenticationAttempt.objects.values_list('id')\
        .filter(ip_address=ip)\
        .filter(user_agent=ua)\
        .count()

    if attempted > 0:
        attempt = AuthenticationAttempt.objects.get(ip_address=ip, user_agent=ua)
        if attempt.count == 3:
            diff = datetime.now(timezone.utc) - attempt.attempt_at
            diff = (diff.seconds//60)%60

            if diff <= 10:
                return ApiResponse({'last_attempt': attempt.attempt_at}, 403)

    user = User.objects.values_list('id')\
        .filter(username=data.get('username'))\
        .count()

    if not user:
        if attempted > 0:
            attempt.count += 1
            attempt.save()
        
        else:
            attempt = AuthenticationAttempt()
            attempt.ip_address = ip
            attempt.user_agent = ua

        attempt.save()
        raise AuthenticationFailed("Authentication failed.")

    user = User.objects.values('id', 'name', 'username', 'password', 'is_active')\
        .get(username=data.get('username'))
    user = User(**user)

    ip = get_client_ip(request)
    ua = get_client_ua(request)

    valid_password = check_password(data.get('password'), user.password)
    if not valid_password:
        if not attempted:
            attempt = AuthenticationAttempt()
            attempt.ip_address = ip
            attempt.user_agent = ua
            attempt.save()
        else:
            if attempt.count < 3:
                diff = datetime.now(timezone.utc) - attempt.attempt_at
                diff = (diff.seconds//60)%60

                if diff <= 10:
                    attempt.count += 1
                elif diff >= 10:
                    attempt.count = 1

                attempt.save()
            else:
                return ApiResponse({'last_attempt': attempt.attempt_at}, 403)

        raise AuthenticationFailed("Authentication failed.")

    else:
        if not user.is_active:
            raise AuthenticationFailed("This user is inactive.")

        if attempted:
            attempt.delete()

    save_auth_data(user, "test")
    serialized = UserSerializer(user, fields = ('id', 'name', 'username'))
    return ApiResponse({
        'user': serialized.data 
    }, 202)

# TODO: usecases.users.create_user
def create_user(request):
    data = {
        'name': str(request.data.get('name')).strip(),
        'username': str(request.data.get('username')).strip(),
        'password': str(request.data.get('password')).strip(),
        'phone_number': str(request.data.get('phone_number')).strip(),
    }

    user = User()
    user.name = data.get('name')
    user.phone_number = data.get('phone_number')
    user.username = data.get('username')
    user.password = make_password(data.get('password'))

    user.save()

    serialized = UserSerializer(user)
    return ApiResponse(serialized.data)

def save_auth_data(user : User, new_token : str, old_token : str = None):
    if old_token:
        auth = AuthenticatedUser()
    else:
        auth = AuthenticatedUser()
        auth.token = make_password(new_token)
        auth.user = user
        
        auth.save()
    
