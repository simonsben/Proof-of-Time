# Proof of Time

Idea is to create a service that can guarantee that someone had a file in its current state at some point in time.
This can be done by making a json string with the digest of the file, and the time it was created.
This string can then be signed.
The signature and info can then be packaged in as a json string and passed back to the requester.


## Guarantee

The package guarantees that the doc existed at the **UTC** datetime listed **IF**:

* the digest matches that of the file it is guaranteeing
* the signature can be verified against the JSON stringified representation of the 'info' block (see below)
* the verification is done using the site's public key


## Package

The generated package has the following form:

```json
{
  "info": {
    "datetime": "UTC datetime",
    "digest": "SHA3-256 digest of file"
  },
  "signature": "Ed448 signature of the above 'info' block",
  "public_key": "Optional, public key to check signature without returning to the site",
  "message": "Optional, message passed with package creation request (ex. 'proof for doc X')"
}
```

## Usage

It is intended that the code is used to make several AWS Lambda functions.
These are one to create the key, one to create a package, and one to verify a package.
To configure this do the following:

* Generate a layer that contains the dependency `cryptography` built for the Lambda environment
    * This can be done using [this](git@github.com:simonsben/lambda_layer_builder.git) code
* Create a function for creating the key, creating a package, and verifying a package
* Assemble and upload the code for the functions by running [`prepare_functions.sh`](./prepare_functions.sh)
* For the first grant it permission to create a secret named `pit_secret`
    * NOTE: Don't grant it permission to modify or delete secrets to prevent accidental overwriting
* For the other two grant permission to read the secret and add the environment variable `secret_name` as `pit_secret`
* Upload and add the layer to each of them
* Specify the handler for each of the functions (i.e. `lambda_handler.lambda_handler` -> `FILE_NAME.handler`)


## Future features

* Cache secret between invocations
