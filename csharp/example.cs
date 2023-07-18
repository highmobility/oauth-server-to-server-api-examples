using Jose; // https://github.com/dvsekhvalnov/jose-jwt
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Xml.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace HMServiceAccountAPISample;
class MainClass
{
    /*
     * Sandbox service account private key json example
     * 
     * {    "inserted_at":"2023-07-17T10:19:10",
     *      "private_key":"-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgbtaDZT7wj9kWE3tn\nkimCOiO4bKmxu74r79DNwn55UHWhRANCAATvFUpSLM6OIGfGXY001+DtKYwdTgWB\nNQF51+kiLN9OF5rRtdExRdivdNEWkcy65H5aV5dm0pB2Dl3/odUcQKgC\n-----END PRIVATE KEY-----",
     *      "instance_uri":"https://sandbox.api.high-mobility.com",
     *      "token_uri":"https://sandbox.api.high-mobility.com/v1/auth_tokens",
     *      "id":"6c912e9b-ac53-4068-81ac-6bf971aba0c5"
     * }
     */

    //For production use production service account private key json values

    //Remove header, footer and newlines from your private key in the snippet        
    static string private_key = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgbtaDZT7wj9kWE3tnkimCOiO4bKmxu74r79DNwn55UHWhRANCAATvFUpSLM6OIGfGXY001+DtKYwdTgWBNQF51+kiLN9OF5rRtdExRdivdNEWkcy65H5aV5dm0pB2Dl3/odUcQKgC";
    //iss is id in service account private key json
    static string iss = "6c912e9b-ac53-4068-81ac-6bf971aba0c5";
    //For production use https://api.high-mobility.com/v1
    static string aud = "https://sandbox.api.high-mobility.com/v1";

    static string createJwtToken()
    {
        var payload = new Dictionary<string, object>()
                {
                    { "iss", iss },
                    { "aud", aud},
                    { "iat", DateTimeOffset.Now.ToUnixTimeSeconds()},
                    { "jti", Guid.NewGuid()},
                    { "ver", 2}
                };

        ECDsa key = ECDsa.Create();
        key.ImportPkcs8PrivateKey(Convert.FromBase64String(private_key), out _);

        string token = Jose.JWT.Encode(payload, key, JwsAlgorithm.ES256);
        return token;
    }

    static string getServiceAccountTokenUsingJwt()
    {
        HttpClient client = new HttpClient();

        //Add request body
        var formContent = new FormUrlEncodedContent(new[]
        {
            new KeyValuePair<string, string>("assertion", createJwtToken()),
        });

        Console.WriteLine(client.DefaultRequestHeaders.ToString());
        HttpResponseMessage response = client.PostAsync(aud + "/auth_tokens", formContent).Result;
        string body = response.Content.ReadAsStringAsync().Result;

        Console.WriteLine(response.ToString());
        Console.WriteLine(body);

        //Parse token from response
        JObject jsonObject = JObject.Parse(body);
        return jsonObject.Value<string>("auth_token");
    }

    static void getFleetVehicles(string token)
    {
        HttpClient client = new HttpClient();

        //Add token as header authenticate Bearer value
        client.BaseAddress = new Uri(aud);
        client.DefaultRequestHeaders.Accept.Clear();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        Console.WriteLine(client.DefaultRequestHeaders.ToString());

        HttpResponseMessage response = client.GetAsync(aud + "/fleets/vehicles").Result;
        string body = response.Content.ReadAsStringAsync().Result;

        Console.WriteLine(response.ToString());
        Console.WriteLine(body);
    }

    static void Main(string[] args)
    {
        string token = getServiceAccountTokenUsingJwt();
        getFleetVehicles(token);
    }
}
