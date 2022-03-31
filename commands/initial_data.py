from applications.users.models import User
from rest_framework.decorators import api_view
from core.utils.response import ApiResponse

master_users = [
    {
        'id': 1,
        'name': 'aziz ruri',
        'username': 'ruriazz',
        'password': 'bcrypt_sha256$$2b$12$sldunOixT5Hc3PmrpjKt8ukFckqBT6qGaKY9NKcP9k5mEII1wNNhS',
        'phone_number': '62',
        'is_active': True
    },
    {
        'id': 2,
        'name': 'elsya arystin',
        'username': 'caee',
        'password': 'bcrypt_sha256$$2b$12$LRSAfdD2YLWkqzpvrv9o3e1nyu7mpeLi0WdGX.2NpWefRndx0aUOe',
        'phone_number': '621',
        'is_active': True
    }
]

@api_view(['GET'])
def master(request):
    for user_dict in master_users:
        user = User.objects.values_list('username')\
        .filter(username=user_dict.get('username'))\
        .count()

        if not user:
            user = User()
            user.id = user_dict.get('id')
            user.name = user_dict.get('name')
            user.username = user_dict.get('username')
            user.password = user_dict.get('password')
            user.phone_number = user_dict.get('phone_number')
            user.is_active = user_dict.get('is_active')

            user.save()

    return ApiResponse('init success..')

    