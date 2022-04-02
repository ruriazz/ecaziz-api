from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from applications.ucapan.models import Ucapan
from applications.users.models import User

from serializers.users import UserSerializer

def get_dashboard_data():
    return ApiResponse({
        'undangans_active': _get_undangans_active(),
        'undangans_info': _get_undangans_info(),
        'undangans_response': _get_undangans_response(),
        'latest_response': _get_latest_response()
    })

def _get_undangans_active():
    return Undangan.objects.only('id')\
        .filter(is_active=True)\
        .values_list('id')\
        .count()

def _get_undangans_info():
    results = []

    users = Undangan.objects.only('created_by')\
        .filter(is_active=True)\
        .values('created_by')\
        .distinct()

    for user in users:
        user = UserSerializer(User.objects.get(id=user['created_by']), fields=('id', 'username', 'name')).data
        user['undangans'] = Undangan.objects.filter(created_by_id=user['id']).count()
        results.append(user)

    return results

def _get_undangans_response():
    return ""

def _get_latest_response():
    return ""