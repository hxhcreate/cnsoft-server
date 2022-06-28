import random
import string
import hashlib
from .rsa_tool import *
from ..config.redis import redis_db


def get_random_string(slen):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


class Token:
    def __init__(self, userID, username="", wechatid=""):
        # user_str_encrypt = hashlib.md5((get_random_string(5) + str(userID)).encode('utf-8')).hexdigest()
        user_str_encrypt = get_random_string(5) + str(userID)
        random_len = random.randint(10, 25)
        random_string = ''.join(random.sample(string.ascii_letters + string.digits, random_len))
        self.token = user_str_encrypt + random_string
        self.token_value = ";".join([str(userID), username, wechatid])

    def deliver_token(self):
        redis_db.handle_redis_token(self.token, self.token_value)
        return self.token

    @staticmethod
    def get_token_value(token):
        return redis_db.handle_redis_token(token).split(';')  # 返回一个列表

    @staticmethod
    def token_is_valid(token):
        return redis_db.exists_key(token)

    @staticmethod
    def delete_token(token):
        redis_db.del_key(token)
