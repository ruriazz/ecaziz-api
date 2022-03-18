from http.client import BAD_REQUEST, CREATED
from core.utils.hash import Hash
from core.utils.response import ApiResponse

from serializers.undangan import UndanganSerializer
from serializers.users import UserSerializer
from applications.undangan.models import Undangan
from usecases.undangan.validate_data import validate_undangan

def create_new_undangan(request):
    validate = validate_undangan(request.data)
    if not validate.get('valid'):
        return ApiResponse(
            data = validate.get('errors'),
            status = BAD_REQUEST
        )

    data = validate.get('data')
    undangan = Undangan(**data)
    undangan.created_by = request.auth.user
    undangan.save()

    link_template = 'BASE_URL/?inv={idencoded}'
    undangan.link = link_template.format(idencoded=Hash.UndanganId().encode(undangan.id))
    undangan.save()
    
    serialized = UndanganSerializer(undangan, fields = ('id', 'undangan_type', 'person_type', 'person_name', 'person_partner', 'person_location', 'phone_number', 'link', 'created_by', 'created_at', 'updated_at', 'is_active'))
    serialized_data = serialized.data
    serialized_data['created_by'] = UserSerializer(undangan.created_by, fields = ('id', 'name')).data

    return ApiResponse(
        data = serialized_data,
        status = CREATED
    )