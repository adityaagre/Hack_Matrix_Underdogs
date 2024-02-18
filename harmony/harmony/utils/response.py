def response_payload(success: bool, data=None, message=None):
    response = {
        "success": success,
    }
    if message is not None:
        response['message'] = message
    if success is True and data is not None:
        response['data'] = data
    elif success is False and data is not None:
        response['errors'] = data

    return response
