from core import verify_package
from utilities import get_private_key


def handler(event, context):
    """

    :param dict event:
    :param dict context:
    :return dict:
    """
    request_parameters = event['queryStringParameters']
    if 'package' not in request_parameters:
        return {
            'statusCode': 400,
            'body': 'Invalid request parameters.'
        }

    package = request_parameters['package']

    private_key_response = get_private_key()
    if 'error' in private_key_response:
        return private_key_response['error']

    private_key = private_key_response['key']
    public_key = private_key.public_key()

    if verify_package(public_key, package):
        return {
            'statusCode': 200,
            'body': {
                'is_valid': True,
                'message': 'Signature is valid.'
            }
        }

    return {
        'statusCode': 200,
        'body': {
            'is_valid': False,
            'message': 'Signature is not valid.'
        }
    }
