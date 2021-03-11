from verify_package import handler
from utilities import *
from json import loads
from core import *

with Path(package_path).open('r') as fl:
    package = loads(fl.read())
print('Package loaded.')

request_data = {
    'queryStringParameters': {
        'package': package
    }
}

verification = handler(request_data, {})
print(
    dumps(verification)
)
