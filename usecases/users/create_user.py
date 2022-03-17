from django.contrib.auth.hashers import make_password
from core.utils.response import ApiResponse
from serializers.users import UserSerializer
from applications.users.models import User

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