import jwt, datetime, time, datetime
from flask import jsonify
from ..models import User
from ..config import SECRET_KEY
from message import *


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time):
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
                    'login_time': login_time
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
            payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        try:
            user = User.select_user_by_username(username)
        except Exception as e:
            print(e)
            return SQLError()
        else:
            if user.check_password(password):
                time_stamp = int(time.time())
                token = self.encode_auth_token(user.id, time_stamp)
                return Success(
                    {"token": token.decode(), "logtime": time.strftime("%Y-%m-%d %H:%M:%S",
                                                                       time.localtime(time_stamp))})
            else:
                return PwdError()

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                return ParamsError()
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    try:
                        user = User.select_user_by_id(payload.data.id)
                    except Exception as e:
                        print(e)
                        return SQLError()
                    if user.login_time == payload['data']['login_time']:
                        return Success()
                    else:
                        return MessageFailed()
                else:
                    return MessageFailed()
        return ParamsError()
