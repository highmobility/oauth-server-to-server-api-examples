# H-M OAuth Server-to-Server API

The OAuth API allows you to create and manage your resources from your own cloud infrastructure.

Once the administrator of your organisation creates an [API key](https://developers.high-mobility.com/api_keys),
our system generates a cryptographic key-pair according to the [JSON Web Token (JWT) standard](https://jwt.io/).

Short overview of the steps:

* Include the key-pair information in your back-end system. You can use your preferred JWT library.
* Create an auth token per example below.
* Use auth token for all endpoints.

You can find sample codes for python and nodejs in this repository.
