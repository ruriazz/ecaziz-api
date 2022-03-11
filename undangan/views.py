from rest_framework.decorators import api_view
from core.helpers.response import ApiResponse

@api_view(['GET'])
def test(request):
    return ApiResponse("mantapps", 403)