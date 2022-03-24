from http.client import OK
from rest_framework.decorators import api_view
from core.utils.handlers import valid_auth
from core.utils.response import ApiResponse
from usecases.users.refresh_auth_token import refresh_auth_token
from usecases.users.user_authentication import user_authentication

class UserViews:

    @api_view(['POST'])
    def authentication(request):
        return user_authentication(request)

    @api_view(['GET'])
    @valid_auth
    def refresh_auth_token(request):
        return ApiResponse(
            headers = {
                'auth-token': request.new_token
            },
            status = OK
        )

