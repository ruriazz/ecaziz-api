from http.client import ACCEPTED, BAD_REQUEST
from applications.ucapan.models import Ucapan
from core.utils.response import ApiResponse
from serializers.ucapan import UcapanSerializer
from serializers.undangan import UndanganSerializer

def update_data_ucapan(data:dict, id:int):
    if not Ucapan.objects.filter(id=id).exists():
        return ApiResponse(
            status = BAD_REQUEST,
            data = 'Data not found.'
        )

    ucapan = Ucapan.objects.get(id=id)
    for i in data.keys():
        setattr(ucapan, i, data.get(i))

    ucapan.save()
    serialized = UcapanSerializer(ucapan, fields = ('id', 'undangan', 'sender', 'text', 'is_active', 'created_at', 'updated_at')).data
    serialized['undangan'] = UndanganSerializer(ucapan.undangan, fields = ('id', 'undangan_type', 'person_name')).data
    return ApiResponse(
        data = serialized,
        status = ACCEPTED
    )