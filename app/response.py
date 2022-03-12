from rest_framework.response import Response

def ApiResponse(data, code : int = 200):
    response = {
        'success': False,
        'code': code,
        'data': data
    }

    if code >= 200 and code <= 206:
        response['success'] = True

    if isinstance(data, str):
        response['message'] = data
        del response['data']

    return Response(response, code)