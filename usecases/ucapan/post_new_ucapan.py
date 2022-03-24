from http.client import BAD_REQUEST, CREATED
from core.utils.response import ApiResponse
from serializers.ucapan import UcapanSerializer
from serializers.undangan import UndanganSerializer
from usecases.ucapan.validate_data import validate_data_ucapan
from applications.ucapan.models import Ucapan

def post_new_ucapan(request):
    validate = validate_data_ucapan(request.data)
    if not validate.get('valid'):
        return ApiResponse(
            data = validate.get('errors'),
            status = BAD_REQUEST
        )

    data = validate.get('data')

    if data.get('undangan').undangan_type == "O" and Ucapan.objects.filter(undangan=data.get('undangan')).exists():
        return ApiResponse(
            data = 'already',
            status = BAD_REQUEST
        )

    elif data.get('undangan').undangan_type == "G" and Ucapan.objects.filter(undangan=data.get('undangan')).count() >= 100:
        return ApiResponse(
            data = 'limit_ucapan',
            status = BAD_REQUEST
        )

    ucapan = Ucapan(**validate.get('data'))
    ucapan.save()

    serialized = UcapanSerializer(ucapan, fields = ('id', 'undangan', 'sender', 'text', 'is_active', 'created_at', 'updated_at'))
    serialized_data = serialized.data
    serialized_data['undangan'] = UndanganSerializer(ucapan.undangan, fields = ('id', 'undangan_type', 'person_name')).data

    return ApiResponse(
        data = serialized_data,
        status = CREATED
    )