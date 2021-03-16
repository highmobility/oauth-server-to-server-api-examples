var fs = require('fs')
var jwt = require('jsonwebtoken')
var request = require('request');

// Get API details
var ACCOUNT_API_CONFIG = {
    version: 2,
    base_url: 'https://sandbox.api.high-mobility.com/v1',
    api_key: '6456a189-7c39-4343-b02a-3ee4c3a63142',
    private_key: "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIEYhNYsWg+Bc8Zt7d9IjKjSeQ+O4NiGaBbjP2eIOMF+ToAoGCCqGSM49\nAwEHoUQDQgAEeCm3pl4WpevWJw/fO0cCjwh2pntgw3Xw7TG6Frrhep/y3mvU18Ks\nwcCucERfkbY9AkPeTXseFC7DsKsexrMk2A==\n-----END EC PRIVATE KEY-----\n\n"
}
var iat = Math.round(Date.now()/1000);

var priv = Buffer.from(ACCOUNT_API_CONFIG.private_key, 'utf8')

var payload = { 'ver': ACCOUNT_API_CONFIG.version, iss: ACCOUNT_API_CONFIG.api_key, 'aud': ACCOUNT_API_CONFIG.base_url, 'iat': iat };
var token = jwt.sign(payload, priv, { algorithm: 'ES256' })

request.post(
    ACCOUNT_API_CONFIG.base_url + '/auth_tokens',
    {form: {'assertion': token}},
    function (error, response, body) {
        console.log('error:', error);
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body);
    }
);
