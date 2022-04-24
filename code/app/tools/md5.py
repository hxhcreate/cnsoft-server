import hashlib
from ..config import MD5_SALT


def encode_md5(string):
    string += MD5_SALT
    md5 = hashlib.md5()
    md5.update(string.encode("utf-8"))
    return md5.hexdigest()  # 返回加密后的密文


def decode_md5():
    return
