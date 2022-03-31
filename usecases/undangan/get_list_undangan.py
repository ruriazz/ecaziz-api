import math
from http.client import OK
from core.utils.response import ApiResponse

from applications.undangan.models import Undangan
from serializers.undangan import UndanganSerializer
from serializers.users import UserSerializer


def get_list_undangan(request):
    page = int(request.query_params.get('page')) if request.query_params.get('page', '').isnumeric() and int(request.query_params.get('page')) > 0 else 1
    index = page - 1
    limit = int(request.query_params.get('limit')) if request.query_params.get('limit', '').isnumeric() else 10
    limit = limit if limit > 0 else 10
    limit = limit if limit <= 100 else 100

    filter_person_name = str(request.query_params.get('person_name')).strip() if request.query_params.get('person_name', '') != '' else None
    filter_created_by = int(request.query_params.get('created_by')) if request.query_params.get('created_by', '').isnumeric() else None
    filter_is_active = int(request.query_params.get('is_active')) if request.query_params.get('is_active', '').isnumeric() else None
    filter_undangan_type = request.query_params.get('undangan_type').upper() if request.query_params.get('undangan_type', '') != '' else None
    search_keywords = str(request.query_params.get('q')).strip() if request.query_params.get('q', '') != '' else None

    undangans = Undangan.objects\
        .order_by('person_name', 'id')\
        .only('id', 'undangan_type', 'person_type', 'person_name', 'person_partner', 'person_location', 'phone_number', 'link', 'created_by', 'created_at', 'updated_at', 'is_active')

    if filter_person_name is not None:
        undangans = undangans.filter(person_name=filter_person_name)

    if filter_created_by is not None:
        undangans = undangans.filter(created_by=filter_created_by)

    if filter_is_active is not None:
        undangans = undangans.filter(is_active=False if filter_is_active == 0 else True)

    if filter_undangan_type is not None:
        undangans = undangans.filter(undangan_type=filter_undangan_type)

    if search_keywords is not None:
        undangans = undangans.filter(person_name__icontains=search_keywords)

    total_rows = undangans.count()
    total_page = math.ceil(total_rows / limit)
    offset = index * limit
    maxidx = (index * limit) + limit

    undangans = undangans[offset:maxidx]
    results = []

    for undangan in undangans:
        serialized = UndanganSerializer(undangan, fields = ('id', 'undangan_type', 'person_type', 'person_name', 'person_partner', 'person_location', 'phone_number', 'link', 'created_by', 'created_at', 'updated_at', 'is_active')).data
        serialized['created_by'] = UserSerializer(undangan.created_by, fields = ('id', 'name')).data

        results.append(serialized)

    return ApiResponse(
        data = {
            'pagination': {
                'current_page': page,
                'limit': limit,
                'total_results': len(results),
                'total_page': total_page,
                'total_rows': total_rows

            },
            'undangans': results
        },
        status = OK
    )
