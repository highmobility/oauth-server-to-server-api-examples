import time
import uuid
import jwt
from jwt.utils import force_bytes
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Get API details
OAUTH_CLIENT_CREDENTIALS_CONFIG = {
    'client_id': 'my-client-id', 
    'client_secret': 'my-secret',
    'instance_uri': 'https://sandbox.api.high-mobility.com' # or in live https://api.high-mobility.com
}



payload = {
    'grant_type': 'client_credentials',
    'client_id': OAUTH_CLIENT_CREDENTIALS_CONFIG['client_id'],
    'client_secret': OAUTH_CLIENT_CREDENTIALS_CONFIG['client_secret'],
}
url = '{}/v1/access_tokens'.format(OAUTH_CLIENT_CREDENTIALS_CONFIG['instance_uri'])
r = requests.post(url, payload, verify=True)
print("api response status: %s" % r.status_code)
print("api response: %s" % r.text)
