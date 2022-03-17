from rest_framework.decorators import api_view
from usecases.users.refresh_auth_token import refresh_auth_token
from usecases.users.user_authentication import user_authentication

class UserViews:

    @api_view(['POST'])
    def authentication(request):
        return user_authentication(request)

    @api_view(['GET'])
    def refresh_auth_token(request):
        return refresh_auth_token(request.headers)

