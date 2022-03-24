from http.client import BAD_REQUEST
from django.core.management.utils import get_random_secret_key
from rest_framework.decorators import api_view
from core.utils.response import ApiResponse
from core.utils.handlers import get_auth, is_authenticated
from usecases.ucapan.delete_data_ucapan import delete_data_ucapan
from usecases.ucapan.post_new_ucapan import post_new_ucapan
from usecases.ucapan.get_list_ucapan import get_list_ucapan
from usecases.ucapan.update_data_ucapan import update_data_ucapan

class UcapanViews:

    @api_view(['GET', 'POST'])
    @get_auth
    def index(request):
        if request.method == 'GET':
            return get_list_ucapan(request)

        elif request.method == 'POST':
            return post_new_ucapan(request)

    @api_view(['DELETE'])
    @is_authenticated
    def posts(request, id:int = None):
        return delete_data_ucapan(id)

    @api_view(['PUT'])
    @is_authenticated
    def status_change(request, id:int):
        print(request.data)
        status = int(request.data.get('is_active')) if str(request.data.get('is_active', '')).isnumeric() else None
        if status is not None and (status == 1 or status == 0):
            return update_data_ucapan({'is_active': status}, id)

        return ApiResponse(
            status = BAD_REQUEST,
            data = 'invalid_status'
        )