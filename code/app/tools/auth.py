import jwt, datetime, time, datetime
from flask import jsonify
from ..models import User, Admin
from ..config import SECRET_KEY
from .message import *
from ..config.redis import redis_db


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time, username="", wechat_id=""):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=0, minutes=10, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': user_id,
                'logtime': login_time,
                'username': username,
                "wechat_id": wechat_id
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, SECRET_KEY,
                             options={'verify_exp': False},
                             algorithms="HS256")
        return payload

    # 判断该auth token 是否存在redis 即是否有效
    @staticmethod
    def identify_auth_header_valid(auth_header):
        auth_tokenArr = auth_header.split(" ")
        if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
            return False
        auth_token = auth_tokenArr[1]
        payload = Auth.decode_auth_token(auth_token)
        _id = payload['data']['id']
        user = User.select_user_by_id(_id)
        if redis_db.exists_key('user' + str(user.id)):
            return True
        return False

    @staticmethod
    def get_identify_info(auth_header):
        """
        用户鉴权
        :return: 返回payload信息
        """
        auth_tokenArr = auth_header.split(" ")
        auth_token = auth_tokenArr[1]
        payload = Auth.decode_auth_token(auth_token)
        return payload['data']
