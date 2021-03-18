import time

import jwt
from jwt.utils import force_bytes
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Get API details
ACCOUNT_API_CONFIG = {
	'version': 1,
	'base_url': 'https://sandbox.api.high-mobility.com/v1',
	'api_key': '6456a189-7c39-4343-b02a-3ee4c3a63142',
         'private_key': """
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEYhNYsWg+Bc8Zt7d9IjKjSeQ+O4NiGaBbjP2eIOMF+ToAoGCCqGSM49
AwEHoUQDQgAEeCm3pl4WpevWJw/fO0cCjwh2pntgw3Xw7TG6Frrhep/y3mvU18Ks
wcCucERfkbY9AkPeTXseFC7DsKsexrMk2A==
-----END EC PRIVATE KEY-----
"""
}

jwt_payload = {
    'ver': ACCOUNT_API_CONFIG['version'],
    'iss': ACCOUNT_API_CONFIG['api_key'],
    'aud': ACCOUNT_API_CONFIG['base_url'],
    'jti': str(uuid.uuid4()),
    'iat': int(time.time()),
}

priv_eckey = load_pem_private_key(force_bytes(ACCOUNT_API_CONFIG['private_key']),
    password=None, backend=default_backend())
jws_message = jwt.encode(jwt_payload, priv_eckey, algorithm='ES256')

assertion = jws_message.decode('utf-8')

payload = {'assertion': assertion}
url = '{}/auth_tokens'.format(ACCOUNT_API_CONFIG['base_url'])
r = requests.post(url, payload, verify=True)
print("api response status: %s" % r.status_code)
print("api response: %s" % r.text)
