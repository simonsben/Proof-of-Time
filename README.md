# Point in time

Idea is to create a service that can guarantee that someone had a file in its current state at some point in time.
This can be done by making a json string with the digest of the file and the time it was created.
This string can then be signed.
The signature and info can then be packaged in as a json string and passed back to the requester.

