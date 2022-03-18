from http.client import BAD_REQUEST, OK
from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from serializers.undangan import UndanganSerializer
from serializers.users import UserSerializer
from usecases.undangan.validate_data import validate_undangan


def update_data_undangan(request, id:int):
    exists = Undangan.objects.filter(id=id).exists()
    if not exists:
        return ApiResponse(
            data = 'Data not found.',
            status = BAD_REQUEST
        )

    validate = validate_undangan(request.data)
    if not validate.get('valid'):
        return ApiResponse(
            data = validate.get('errors'),
            status = BAD_REQUEST
        )

    data = validate.get('data')
    old_undangan = Undangan.objects.get(id=id)
    undangan = Undangan(**data)
    undangan.id = id
    undangan.created_by = old_undangan.created_by
    undangan.created_at = old_undangan.created_at
    undangan.link = old_undangan.link
    undangan.save()

    serialized = UndanganSerializer(undangan, fields = ('id', 'undangan_type', 'person_type', 'person_name', 'person_partner', 'person_location', 'phone_number', 'link', 'created_by', 'created_at', 'updated_at', 'is_active'))
    serialized_data = serialized.data
    serialized_data['created_by'] = UserSerializer(undangan.created_by, fields = ('id', 'name')).data

    return ApiResponse(
        data = serialized_data,
        status = OK
    )