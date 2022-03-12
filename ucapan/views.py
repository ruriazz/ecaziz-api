from rest_framework.decorators import api_view
from app.response import ApiResponse

@api_view(['GET'])
def test(request):
    return ApiResponse("sip", 202)