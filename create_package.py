from utilities import get_private_key, output_public_key, parse_request_parameters
from core import create_package


def handler(event, context):
    """
    Create package function in the form of an AWS Lambda handler

    :param dict event: Web event triggering function
    :param dict context: Information about the execution environment
    :return dict: Package
    """
    request_parameters = parse_request_parameters(event)
    if 'digest' not in request_parameters:
        return {
            'statusCode': 400,
            'body': 'Invalid request parameters.'
        }

    # Retrieve private key and create package
    private_key_response = get_private_key()
    if 'error' in private_key_response:
        return private_key_response['error']

    private_key = private_key_response['key']
    package = create_package(private_key, request_parameters['digest'])

    # TODO consider whether this should be included, would be easier to spoof/fool
    # Optionally, add public key and message to package for client's usage
    if 'include_public_key' in request_parameters and request_parameters['include_public_key']:
        public_key = private_key.public_key()
        package['public_key'] = output_public_key(public_key).decode()

    if 'message' in request_parameters and request_parameters['message']:
        package['message'] = request_parameters['message']

    return package
