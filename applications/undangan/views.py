from rest_framework.decorators import api_view
from core.utils.response import ApiResponse

@api_view(['GET'])
def test(request):
    return ApiResponse("test", 403)