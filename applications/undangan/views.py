from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from core.utils.hash import Hash
from core.utils.handlers import get_auth, is_authenticated
from usecases.undangan.create_new_undangan import create_new_undangan
from usecases.undangan.delete_data_undangan import delete_data_undangan
from usecases.undangan.get_detail_undangan import get_detail_undangan
from usecases.undangan.get_list_undangan import get_list_undangan
from usecases.undangan.update_data_undangan import update_data_undangan

class UndanganViews:

    @api_view(['GET', 'POST'])
    @is_authenticated
    def index(request):
        if request.method == 'POST':
            return create_new_undangan(request)

        elif request.method == 'GET':
            return get_list_undangan(request)

    @api_view(['GET', 'PATCH', 'DELETE'])
    @get_auth
    def info(request, id:int = None, hashid:str = None):
        if request.method == 'GET':
            if hashid is not None:
                id = Hash.UndanganId().decode(hashid)
            
            return get_detail_undangan(id)

        elif request.method == 'PATCH':
            if request.auth is None:
                raise AuthenticationFailed('Authentication credential required.')
            
            return update_data_undangan(request, id)

        elif request.method == 'DELETE':
            if request.auth is None:
                raise AuthenticationFailed('Authentication credential required.')
            
            return delete_data_undangan(id)