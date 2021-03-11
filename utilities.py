from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.hazmat.primitives import serialization
from pathlib import Path


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

    :param ed448.Ed448PublicKey public_key:
    :return bytes:
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

    with file_path.open('wb') as fl:
        fl.write(
            output_private_key(private_key)
        )


def load_private_key(file_path):
    """
    Load private key from file

    :param Path file_path: Path to file
    :return ed448.Ed448PrivateKey: Private key object
    """
    with file_path.open('rb') as fl:
        return serialization.load_pem_private_key(
            data=fl.read(),
            password=None
        )
