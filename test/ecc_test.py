from utilities import *
from core import *
from time import sleep
from datetime import datetime

private_key = generate_private_key()
public_key = private_key.public_key()

print('Generated private key')
print(output_private_key(private_key).decode())

print('Generated public key')
print(output_public_key(public_key).decode())

save_private_key(private_key, private_key_path)

digest = digest_data('this is the thing i want to digest'.encode())

package = create_package(private_key, digest)

print(package)
print(verify_package(public_key, package))

sleep(2)
package['info']['datetime'] = datetime.now().strftime(datetime_format)
print(package)
print(verify_package(public_key, package))
