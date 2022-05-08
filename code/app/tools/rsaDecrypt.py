import rsa
import base64
from rsa import PublicKey, PrivateKey
import sys

sys.path.append('..')

from config import PRIVATE_KEY, PUBLIC_KEY


# 将上一级的目录加入到import目录中


def rsa_encrypt(d_str):
    # 将字符串进行编码
    content = d_str.encode('utf-8')
    # 加载公匙
    public_key = PublicKey.load_pkcs1_openssl_der(base64.b64decode(PUBLIC_KEY))
    # 公钥加密
    crypto = rsa.encrypt(content, public_key)
    return crypto


def rsa_decrypt(crypto):
    private_key = PrivateKey._load_pkcs1_der(base64.b64decode(PRIVATE_KEY))
    content = rsa.decrypt(crypto, private_key)
    result = content.decode('utf-8')
    return result


if __name__ == "__main__":
    print(rsa_decrypt(rsa_encrypt("123456789")))
