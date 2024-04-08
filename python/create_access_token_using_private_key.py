import time
import uuid
import jwt
from jwt.utils import force_bytes
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Get API details
OAUTH_CLIENT_ASSERTION_CONFIG = {
    'client_id': 'my-client-id', 
    'private_key': "-----BEGIN PRIVATE KEY-----\n....\n-----END PRIVATE KEY-----",
    'id': 'f6c331c4-9271-4e3b-a8c4-6a2cacac6451',
    'instance_uri': 'https://sandbox.api.high-mobility.com' # or in live https://api.high-mobility.com
}


jwt_payload = {
    'ver': 2,
    'iss': OAUTH_CLIENT_ASSERTION_CONFIG['id'],
    'aud': '%s/v1' % OAUTH_CLIENT_ASSERTION_CONFIG['instance_uri'],
    'jti': str(uuid.uuid4()),
    'iat': int(time.time()),
}

priv_eckey = load_pem_private_key(force_bytes(OAUTH_CLIENT_ASSERTION_CONFIG['private_key']),
    password=None, backend=default_backend())
jws_message = jwt.encode(jwt_payload, priv_eckey, algorithm='ES256')

client_assertion = jws_message.decode('utf-8')

payload = {
    'client_id': OAUTH_CLIENT_ASSERTION_CONFIG['client_id'],
    'client_assertion': client_assertion,
    'grant_type': 'client_credentials',
    'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
}
url = '{}/v1/access_tokens'.format(OAUTH_CLIENT_ASSERTION_CONFIG['instance_uri'])
r = requests.post(url, payload, verify=True)
print("api response status: %s" % r.status_code)
print("api response: %s" % r.text)
