from create_package import handler
from utilities import *
from core import *

request_data = {
    'queryStringParameters': {
        'digest': digest_data('some data to digest'.encode()),
        'message': 'test_file',
        'include_public_key': True
    }
}
print(f'Making request with\n {dumps(request_data)}')

package = handler(request_data, {})

print(
    dumps(package)
)

with Path(package_path).open('w') as fl:
    fl.write(
        dumps(package)
    )
print('Package saved')
