from users.models import User
from rest_framework.decorators import api_view
from core.utils.response import ApiResponse

@api_view(['GET'])
def master(request):
    user = User.objects.values_list('id')\
        .filter(id=1)\
        .count()

    if not user:
        user = User()
        user.id = 1
        user.name = 'aziz ruri suparman'
        user.username = 'ruriazz'
        user.password = 'bcrypt_sha256$$2b$12$S/mPQh4H60bNGQKo6FjJV.RnA2Yi24bdiOF/xvA/g28jeMttxIw5y'
        user.phone_number = '62'
        user.is_active = True

        user.save()
        return ApiResponse("Init success.")

    return ApiResponse()

    