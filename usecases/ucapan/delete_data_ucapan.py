from http.client import ACCEPTED, BAD_REQUEST
from applications.ucapan.models import Ucapan
from core.utils.response import ApiResponse
from serializers.ucapan import UcapanSerializer
from serializers.undangan import UndanganSerializer


def delete_data_ucapan(id:int):
    if not Ucapan.objects.filter(id=id).exists():
        return ApiResponse(
            data = 'Data not found.',
            status = BAD_REQUEST
        )

    ucapan = Ucapan.objects.get(id=id)
    ucapan.soft_delete()
    serialized = UcapanSerializer(ucapan, fields = ('id', 'undangan', 'sender', 'text', 'is_active', 'created_at', 'updated_at')).data
    serialized['undangan'] = UndanganSerializer(ucapan.undangan, fields = ('id', 'undangan_type', 'person_name')).data
    return ApiResponse(
        data = serialized,
        status = ACCEPTED
    )