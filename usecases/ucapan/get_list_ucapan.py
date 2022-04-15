import math
from http.client import NO_CONTENT, OK
from django.db.models import Q
from applications.ucapan.models import Ucapan
from applications.undangan.models import Undangan
from core.utils.response import ApiResponse
from serializers.ucapan import UcapanSerializer
from serializers.undangan import UndanganSerializer

def get_list_ucapan(request):
    page = int(request.query_params.get('page')) if str(request.query_params.get('page', '')).isnumeric() and int(request.query_params.get('page')) > 0 else 1
    index = page - 1
    limit = int(request.query_params.get('limit')) if str(request.query_params.get('limit', '')).isnumeric() else 5
    limit = limit if limit > 0 else 5
    limit = limit if limit <= 100 else 50

    filter_is_active = int(request.query_params.get('is_active')) if str(request.query_params.get('is_active', '')).isnumeric() else None
    filter_keywords = str(request.query_params.get('q')).strip() if request.query_params.get('q', '') != '' else None

    ucapans = Ucapan.objects\
        .only('id', 'undangan', 'sender', 'text', 'is_active', 'created_at', 'updated_at')\
        .order_by('-created_at', '-id')

    if not request.auth:
        filter_is_active = True
        filter_keywords = None

        undangans = Undangan.objects\
            .filter(is_active=True)\
            .values('id')

        filter_undangan = []
        for undangan in undangans:
            undangan = Undangan(**undangan)
            filter_undangan.append(undangan)

        ucapans = ucapans.filter(undangan__in=filter_undangan)

    if filter_is_active is not None:
        ucapans = ucapans.filter(is_active = filter_is_active)

    if filter_keywords is not None and len(filter_keywords) > 0:
        ucapans = ucapans.filter(Q(sender__contains=filter_keywords) | Q(text__contains=filter_keywords))

    total_rows = ucapans.count()
    total_page = math.ceil(total_rows / limit)
    offset = index * limit
    maxidx = (index * limit) + limit

    ucapans = ucapans[offset:maxidx]
    results = []

    for ucapan in ucapans:
        attend = True if ucapan.text.split(' +_~_+ ')[0] == 'attend' else False
        message = ucapan.text.split(' +_~_+ ')[1]
        serialized = UcapanSerializer(ucapan, fields = ('id', 'undangan', 'sender', 'is_active', 'created_at', 'updated_at')).data
        serialized['attend'] = attend
        serialized['message'] = message    
        serialized['undangan'] = UndanganSerializer(ucapan.undangan, fields = ('id', 'undangan_type', 'person_name')).data

        results.append(serialized)

    status = NO_CONTENT if len(results) < 1 else OK
    return ApiResponse(
        data = {
            'pagination': {
                'current_page': page,
                'limit': limit,
                'total_results': len(results),
                'total_page': total_page,
                'total_rows': total_rows

            },
            'ucapans': results
        },
        status = status
    )