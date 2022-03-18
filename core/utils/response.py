import datetime
from http.client import IM_USED, NO_CONTENT, OK
from rest_framework.response import Response

def ApiResponse(data = None, status : int = OK, headers : dict = {}):
    response = {
        'success': False,
        'code': status
    }

    if data:
        response['content'] = data

    if status >= OK and status <= IM_USED:
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
    status = status if data is not None else NO_CONTENT
    return Response(data=response, status=status, headers=headers)