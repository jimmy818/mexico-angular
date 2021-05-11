from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print('context', context)
    print('response', response)
    print('exc', exc)

    # check that a ValidationError exception is raised
    if isinstance(exc, AuthenticationFailed):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        response.data = {
            'message': 'Sesión no autorizada o ha caducado',
            'code': 1001
        }
        response.status_code = 401

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['status_code'] = response.status_code
    if response is not None:
        message = 'Ha ocurrido algo'
        data = response.data
        response.data = {}
        errors = []

        try:
            for field, value in data.items():
                errors.append('{}'.format(''.join(value)))
                # errors.append("{}:{}".format(field, " ".join(value)))
        except Exception as e:
            for value in data:
                errors.append('{}'.format(''.join(value)))

        response.data['message'] = message
        response.data['errors'] = errors
        response.data['exception'] = str(exc)
        # print(exc.get_codes())

    return response
