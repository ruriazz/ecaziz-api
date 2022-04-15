from http.client import BAD_REQUEST, OK
from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from applications.ucapan.models import Ucapan
from serializers.undangan import UndanganSerializer
from serializers.users import UserSerializer
from serializers.ucapan import UcapanSerializer


def get_detail_undangan(id:int):
    exists = Undangan.objects.filter(id=id).exists()
    if not exists:
        return ApiResponse(
            data = 'Data not found.',
            status = BAD_REQUEST
        )

    undangan = Undangan.objects.get(id=id)
    serialized = UndanganSerializer(undangan, fields = ('id', 'undangan_type', 'person_type', 'person_name', 'person_partner', 'person_location', 'phone_number', 'link', 'created_by', 'created_at', 'updated_at', 'is_active'))
    serialized_data = serialized.data
    serialized_data['created_by'] = UserSerializer(undangan.created_by, fields = ('id', 'name')).data

    current_response = []
    responses = Ucapan.objects\
        .filter(undangan_id=undangan.id)\
        .order_by('-created_at')

    for response in responses:
        attend = True if response.text.split(' +_~_+ ')[0] == 'attend' else False
        message = response.text.split(' +_~_+ ')[1]
        response = UcapanSerializer(response, fields = ('id', 'sender', 'is_active', 'created_at', 'updated_at')).data
        response['attend'] = attend
        response['message'] = message

        current_response.append(response)

    if len(current_response) > 0:
        serialized_data['response'] = current_response

    return ApiResponse(
        data = serialized_data,
        status = OK
    )