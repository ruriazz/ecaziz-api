import datetime
from rest_framework.response import Response

def ApiResponse(data = None, code : int = 200):
    response = {
        'success': False,
        'code': code
    }

    if data:
        response['content'] = data

    if code >= 200 and code <= 206:
        response['success'] = True
    else:
        del response['content']
        response['errors'] = data

    if data and isinstance(data, str):
        if 'content' in response:
            del response['content']
        else:
            del response['errors']

        response['message'] = data

    response['time'] = datetime.datetime.now()
    return Response(response, code)