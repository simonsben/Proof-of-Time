# Point in time

Idea is to create a service that can guarantee that someone had a file in its current state at some point in time.
This can be done by making a json string with the digest of the file, and the time it was created.
This string can then be signed.
The signature and info can then be packaged in as a json string and passed back to the requester.


## Guarantee

The package guarantees that the doc existed at the datetime listed **IF**:

* the UTC datetime matches the expected local time
* the digest matches that of the file it is guaranteeing
* the signature can be verified against the JSON stringified representation of the 'info' block (see below)
* the verification is done using the site's public key


## Package

The generated package has the following form:

```json
{
  "info": {
    "datetime": "UTC datetime",
    "digest": "SHA-256 digest of file"
  },
  "signature": "Ed448 signature of the above 'info' block",
  "public_key": "Optional, public key to check signature without returning to the site",
  "message": "Optional, message passed with package creation request (ex. 'proof for doc X')"
}
```
