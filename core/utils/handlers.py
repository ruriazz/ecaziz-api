from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
from core.utils.hash import JWT

from core.utils.response import ApiResponse

# TODO: core.utils.handlers.custom_exception
def custom_exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response = ApiResponse(response.data.get('detail'), response.status_code)

    return response

# TODO: core.utils.handlers.is_authenticated
def is_authenticated(function):
    def wrapper(request, *args, **kwargs):

        token = get_credentials(request)
        if not token:
            raise AuthenticationFailed('No authentication credentials.')

        verified = JWT.verify(token)
        if not verified:
            raise AuthenticationFailed('Invalid authentication credentials.')
        
        request.auth = verified

        func = function(request, *args, **kwargs)
        return func

    return wrapper

# TODO: 
def get_auth(function):
    def wrapper(request, *args, **kwargs):
        auth = None
        token = get_credentials(request)
        if token:
            verified = JWT.verify(token)
            auth = verified if verified else auth

        request.auth = auth
        func = function(request, *args, **kwargs)
        return func

    return wrapper

# TODO: 
def valid_auth(function):
    def wrapper(request, *args, **kwargs):
        token = get_credentials(request)
        if not token:
            raise AuthenticationFailed('No authentication credentials.')

        new_token = JWT.refresh(token)
        if not new_token:
            raise AuthenticationFailed('Invalid authentication credentials.')

        request.new_token = new_token

        func = function(request, *args, **kwargs)
        return func

    return wrapper

# TODO: core.utils.handlers.get_credentials
def get_credentials(request):
        try:
            return request.headers.get('Authorization').strip().split('Bearer ')[1]
        except:
            return False

# TODO: core.utils.handlers.get_client_ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# TODO: core.utils.handlers.get_client_ua
def get_client_ua(request):
    return request.META.get('HTTP_USER_AGENT')