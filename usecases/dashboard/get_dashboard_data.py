from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from applications.ucapan.models import Ucapan
from applications.users.models import User

from serializers.users import UserSerializer
from serializers.undangan import UndanganSerializer
from serializers.ucapan import UcapanSerializer

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
    undangan = Ucapan.objects.only('undangan_id')\
        .values_list('undangan_id')

    return {
        'total_undangan': len(undangan.distinct()),
        'total_response': len(undangan)
    }

def _get_latest_response():
    ucapans = Ucapan.objects.filter(is_active=True).order_by('-id')[:5]

    results = []

    for ucapan in ucapans:
        attend = True if ucapan.text.split(' +_~_+ ')[0] == 'attend' else False
        message = ucapan.text.split(' +_~_+ ')[1]
        serialized = UcapanSerializer(ucapan, fields = ('id', 'undangan', 'sender', 'is_active', 'created_at', 'updated_at')).data
        serialized['attend'] = attend
        serialized['message'] = message    
        serialized['undangan'] = UndanganSerializer(ucapan.undangan, fields = ('id', 'undangan_type', 'person_name')).data

        results.append(serialized)

    return results