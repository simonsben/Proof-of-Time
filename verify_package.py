from core import verify_package
from utilities import get_private_key, parse_request_parameters


def handler(event, context):
    """
    Verify package function in the form of an AWS Lambda handler

    :param dict event: Web event triggering function
    :param dict context: Information about the execution environment
    :return dict: Verification info
    """
    request_parameters = parse_request_parameters(event)
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
            'is_valid': True,
            'message': 'Signature is valid.'
        }

    return {
        'is_valid': False,
        'message': 'Signature is not valid.'
    }
