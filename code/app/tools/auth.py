import jwt, datetime, time, datetime
from flask import jsonify
from ..models import User
from ..config import SECRET_KEY
from .message import *
from ..config.redis import redis_db


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time, platform, type):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=0, minutes=10, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'logtime': login_time,
                    "pt": platform,
                    "type": type
                }
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp': True})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    @staticmethod
    def authenticate(self, ori_encrypt, password):
        if User.check_password(password, ori_encrypt):
            return True
        return False

    @staticmethod
    def identify(auth_header):
        """
        用户鉴权
        :return: 错误返回jsonify  正确返回用户信息
        """
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                return ERROR(msg='请传递正确的请求消息头')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = User.select_user_by_id(payload['data']['id'])
                    if isinstance(user, None):
                        return ERROR(msg='未找到该用户')
                    if not redis_db.exists_key('user' + str(user.id)):
                        return ERROR(msg='用户没有登录')
                    return payload['data']
                else:
                    return ERROR(msg=payload)
        return ERROR(msg="未提供认证token")
