from utilities import generate_private_key, output_private_key, aws_secret_name
from botocore.exceptions import ClientError
from boto3 import client
from json import dumps


def handler(event, context):
    private_key = generate_private_key()

    private_key_output = output_private_key(private_key)

    secret_client = client('secretsmanager')

    try:
        creation_response = secret_client.create_secret(
            Name=aws_secret_name,
            SecretBinary=private_key_output
        )
        print(dumps(creation_response))

    except ClientError as e:
        print(dumps(e.response))
