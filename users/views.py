from rest_framework.decorators import api_view
from core.utils.response import ApiResponse
from .usecases import create_user, user_authentication

class UserViews:

    @api_view(['POST'])
    def authentication(request):
        return user_authentication(request)
