from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from datetime import datetime
from pathlib import Path
from json import dumps

datetime_format = '%Y-%m-%d %H:%M:%SZ'


def sign_data(private_key, data):
    """

    :param ed448.Ed448PrivateKey private_key:
    :param str data:
    :return bytes:
    """

    return private_key.sign(data.encode())


def verify_data(public_key, signature, data):
    """

    :param ed448.Ed448PublicKey public_key:
    :param bytes signature: Signature of data
    :param str data: Data to check for match with signature
    :return bool: Whether the signature and data match
    """
    try:
        public_key.verify(signature, data.encode())
    except InvalidSignature:
        return False

    return True


def digest_data(data):
    """
    Compute the hash of the passed data

    :param bytes data: Data to be hashed
    :return str: Hex of data digest
    """
    data_hash = hashes.Hash(hashes.SHA3_256())
    data_hash.update(data)

    return data_hash\
        .finalize()\
        .hex()


def digest_file(file_path):
    """
    Compute the digest of a given file

    :param Path file_path: Path to the file being digested
    :return bytes: File digest
    """

    with file_path.open('rb') as fl:
        return digest_data(fl.read())


def create_package(private_key, digest):
    """
    Create a package of info showing a file existed at a given time

    :param ed448.Ed448PrivateKey private_key:
    :param str digest:
    :return dict: Dict with time, digest, and signature
    """
    info = {
        'datetime': datetime.utcnow().strftime(datetime_format),
        'digest': digest
    }

    package = {
        'info': info,
        'signature': sign_data(private_key, dumps(info)).hex()
    }

    return package


def verify_package(public_key, package):
    """
    Check whether the provided package has been modified

    :param ed448.Ed448PublicKey public_key:
    :param dict package:
    :return :
    """
    signature = bytes.fromhex(package['signature'])
    data = dumps(package['info'])

    return verify_data(public_key, signature, data)
