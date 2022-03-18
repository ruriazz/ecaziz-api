from datetime import datetime, timezone
from http.client import ACCEPTED
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password

from core.utils.response import ApiResponse
from core.utils.handlers import get_client_ip, get_client_ua
from core.utils.hash import JWT
from applications.users.models import AuthenticationAttempt, User
from serializers.users import UserSerializer

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

    auth_token = JWT.build(user)
    serialized = UserSerializer(user, fields = ('id', 'name', 'username'))

    return ApiResponse(
        data = {
            'user': serialized.data 
        },
        headers = {
            'Auth-Token': auth_token
        },
        status = ACCEPTED
    )