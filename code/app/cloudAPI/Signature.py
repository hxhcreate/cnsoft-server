import uuid
import time
import copy
import hmac
import urllib.parse
from hashlib import sha1
from hashlib import sha256
import requests

accesskey = 'e74480e45cd5404aa72d6c536e1f3933'
secretkey = '25c9f0e30e0d4ba6aa4c6b302985f8cf'
host = 'https://api-wuxi-1.cmecloud.cn:8443'


def percent_encode(encode_str):
    encode_str = str(encode_str)
    res = urllib.parse.quote(encode_str.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def sign(http_method, access_key, secret_key, servlet_path):
    querystring = {"AccessKey": access_key, "Timestamp": "example_time_stamp", "Signature": "",
                   "SignatureMethod": "HmacSHA1", "SignatureNonce": str(uuid.uuid4()), "SignatureVersion": "V2.0"}
    timestr = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    querystring['Timestamp'] = timestr
    parameters = copy.deepcopy(querystring)
    parameters.pop("Signature")
    sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalized_query_string = ""
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&' + percent_encode(k) + '=' + percent_encode(v)

    string_to_sign = http_method + '\n' \
                     + percent_encode(servlet_path) + '\n' \
                     + sha256(canonicalized_query_string[1:].encode('utf-8')).hexdigest()

    key = ('BC_SIGNATURE&' + secret_key).encode('utf-8')
    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(key, string_to_sign, sha1).hexdigest()
    querystring['Signature'] = signature
    return querystring


def get_fullurl(method, url):
    querystring = sign(method, accesskey, secretkey, url)
    params = ''
    for (k, v) in querystring.items():
        params += str(k) + '=' + str(v) + '&'
    params = params[:-1]
    fullurl = host + url + '?' + params
    s = requests.session()
    s.keep_alive = False
    return fullurl
