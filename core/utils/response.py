import datetime
from rest_framework.response import Response

def ApiResponse(data = None, status : int = 200, headers : dict = {}):
    response = {
        'success': False,
        'code': status
    }

    if data:
        response['content'] = data

    if status >= 200 and status <= 206:
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
    return Response(data=response, status=status, headers=headers)