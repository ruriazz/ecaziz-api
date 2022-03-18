from http.client import BAD_REQUEST, OK
from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from serializers.undangan import UndanganSerializer
from serializers.users import UserSerializer


def delete_data_undangan(id):
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
    undangan.soft_delete()
    
    return ApiResponse(
        data = serialized_data,
        status = OK
    )