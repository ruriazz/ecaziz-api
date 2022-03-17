from rest_framework.decorators import api_view
from core.utils.response import ApiResponse

@api_view(['GET'])
def test(request):
    return ApiResponse("sip", 202)