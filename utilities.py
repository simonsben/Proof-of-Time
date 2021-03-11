from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.hazmat.primitives import serialization
from pathlib import Path
from os import environ


aws_secret_name = 'pit_secret'
private_key_path = 'private.pem'
package_path = 'package.json'


def generate_private_key():
    """
    Generate an ECC private key object

    :return ed448.Ed448PrivateKey: Private key object
    """

    return ed448.Ed448PrivateKey.generate()


def compute_public_key(private_key):
    """
    Compute the public key using the private key

    :param ed448.Ed448PrivateKey private_key: Private key object
    :return ed448.Ed448PublicKey: Public key object
    """

    return private_key.public_key()


def output_private_key(private_key):
    """
    Compute the byte representation of the private key in PEM format

    :param ed448.Ed448PrivateKey private_key: Private key object
    :return bytes: Byte array representing the private key
    """

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def output_public_key(public_key):
    """
    Compute the byte representation of the public key in PEM format

    :param ed448.Ed448PublicKey public_key: Public key object
    :return bytes: Byte representation of the public key
    """

    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def save_private_key(private_key, file_path):
    """
    Output and save private key at the given path

    :param ed448.Ed448PrivateKey private_key: Private key object
    :param Path file_path: Path to save private key
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with file_path.open('wb') as fl:
        fl.write(
            output_private_key(private_key)
        )


def load_private_key(file_path):
    """
    Load private key from file

    :param str file_path: Path to file
    :return ed448.Ed448PrivateKey: Private key object
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with file_path.open('rb') as fl:
        return serialization.load_pem_private_key(
            data=fl.read(),
            password=None
        )


# TODO Write this
def retrieve_private_key(secret_arn):
    """
    Retrieve private key from aws secret manager

    :param str secret_arn: ARN for the secret (i.e. private key)
    :return str: Private key
    """
    raise NotImplementedError('To-do')


def get_private_key(file_path=None):
    """
    Get the private key from a local file or AWS secrets manager

    :param str file_path: Local file path
    :return dict: Private key or error
    """
    if 'secret_arn' in environ:
        return {
            'key': retrieve_private_key(environ['secret_arn'])
        }

    if file_path is None:
        file_path = Path(private_key_path)
    elif isinstance(file_path, str):
        file_path = Path(file_path)

    if file_path and file_path.exists():
        return {
            'key': load_private_key(file_path)
        }

    return {
        'error': {
            'statusCode': 500,
            'body': 'Internal error, please try again later.'
        }
    }
