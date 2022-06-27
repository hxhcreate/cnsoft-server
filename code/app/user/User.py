import time
import json
import requests
from ..tools.auth import Auth
from ..config.redis import redis_db
from ..models import create_pure_user, User, UserLog
from ..tools.error import *
from ..models import WeUserToken, db, WeUserInfo
from ..config import app_id, secret

from flask import jsonify




def get_token(user_id, username="", wechat_id=""):
    time_stamp = int(time.time())
    token = Auth.encode_auth_token(user_id, time_stamp, username, wechat_id)
    print(token)
    redis_db.handle_redis_token("user" + str(user_id), token)
    return token


# 传统注册方式
"""
正确：返回token
错误：抛出错误
"""

def grant_pure(username, password, auth_token=""):
    if auth_token == "":  # 如果不带有auth_token 认为是首次注册
        if User.is_exist_user_by_username(username):
            raise RegisterError("用户名已经存在，不能重复注册")
        else:
            user = create_pure_user(username, password)
            return get_token(user.id, username=user.username, wechat_id=user.wechat_id)
    else:
        if not Auth.identify_auth_header_valid(auth_token):
            raise TokenValidError("auth_header验证失败")
        else:  # token有效
            token_info = Auth.get_identify_info(auth_token)
            _wechat_id = token_info['wechat_id']
            _username = token_info['username']
            _id = token_info['id']
            if _id and _username:
                raise RegisterError("用户名已经存在，不能重复注册")
            if _wechat_id:  # 如果微信存在，则为该用户增加pure信息
                user: User = User.select_user_by_wechat_id(_wechat_id)
                user.username = username
                user.password = password
                User.add(user)
                return get_token(user.id, user.username,user.wechat_id)
            raise RegisterError("该token正确却不含有pure或WeChat的任何一种信息")


"""
传统登录方式
"""


def login_pure(username, password):
    if not User.is_exist_user_by_username(username):
        raise LoginPureError("该用户名不存在，不能直接登录")
    user: User = User.is_exist_user_by_username(username)
    if User.check_password(password, user.password):
        return get_token(user.id, username, user.wechat_id)
    raise LoginPureError("用户密码验证失败")


"""
微信授权
"""


def refresh_token(we_user_token: WeUserToken):
    # 判断失效才获取
    valid_url = 'https://api.weixin.qq.com/sns/auth?' \
                'access_token=%s&' \
                'openid=%s' % (we_user_token.access_token, we_user_token.openid)
    if not json.loads(requests.get(valid_url).text)['errcode']:
        refresh_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?' \
                      'appid=%s&' \
                      'grant_type=refresh_token&' \
                      'refresh_token=%s' % (app_id, we_user_token.refresh_token)
        res_data = json.loads(requests.get(refresh_url).text)
        we_user_token.access_token = res_data['access_token']
        we_user_token.refresh_token = res_data['refresh_token']


def get_we_user_info(we_user_token: WeUserToken):
    info_url = 'https://api.weixin.qq.com/sns/userinfo?' \
               'access_token=%s&' \
               'openid=%s&' \
               'lang=zh_CN' % (we_user_token.access_token, we_user_token.openid)
    res_data = json.loads(requests.get(info_url).text)
    return res_data


def grant_wechat(code, auth_token):
    if code:
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                    "appid={:s}&" \
                    "secret={:s}&" \
                    "code={:s}&" \
                    "grant_type={:s}".format(app_id, secret, code, "authorization_code")
        res_data = json.loads(requests.get(token_url).text)
        user = User.query.filter_by(wechat_id=res_data['unionid']).first()
        if user is None:  # 没有授权 需要判断是新开用户还是旧用户写入信息
            # 先在微信表中insert
            we_user_token = WeUserToken(openid=res_data['openid'], access_token=res_data['access_token'],
                                        refresh_token=res_data['refresh_token'], unionid=res_data['unionid'])
            db.session.add(we_user_token)
            db.session.commit()
            info_data = get_we_user_info(we_user_token)
            we_user_info = WeUserInfo(**info_data)
            db.session.add(we_user_info)
            db.session.commit()
            if auth_token is "":   # 认为是新用
                user = User(wechat_id=res_data['unionid'], nickname=res_data['nickname'],
                            gender=res_data['sex'], province=res_data['province'],
                            city=res_data['city'], country=res_data['country'],
                            avatar=res_data['headimgurl'])
                User.add(user)
                return get_token(user.id, user.username, user.wechat_id)
            else:  # 有token 且没有授权过，则一定是username注册过的，只需要天机即可
                payload = Auth.get_identify_info(auth_token)
                id = payload['id']
                user_from_id: User = User.select_user_by_id(id)
                user_from_id.wechat_id = payload['wechat_id']
                return get_token(user_from_id.id, user_from_id.username,
                                 user_from_id.wechat_id)
        else:  # unionid已经存在
            token = get_token(user.id, user.username, user.wechat_id)
            return token
    else:  # 带token
        raise WechatGrandError("未收到code")
