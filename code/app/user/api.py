import time
import datetime
import requests
import json

from flask import request, jsonify, session, make_response

from . import user
from .User import *
from ..models import User, db, WeUserToken, WeUserInfo
from .wechat import *
from ..tools.decoration import login_required

from ..config import app_id, secret
from ..config.redis import redis_db
from ..tools.auth import Auth
from ..tools.token import Token
# from ..config.es import es

from ..tools.message import *

# 只在APP上存在
""""
无token, 第一次注册通过Pure
有token, token中含有username, 错误
有token， token中含有wechat,认为是该用户的授权
"""


@user.route("/register", methods=['POST'])
def user_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("pwd", "").strip()
        token = request.cookies.get("cookies", "").strip()
        if User.is_exist_user_by_username(username):
            return jsonify(msg='duplicate username, failed!', code=400)

        if token is "":  # 不携带token
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify(msg='register new with pure, success!', code=200)
        else:  # 携带token
            if not Token.token_is_valid(token):
                return jsonify(msg='token invalid, failed!', code=400)
            token_value = Token.get_token_value(token)
            token_userid, token_username, token_wechatid = token_value[0], \
                                                           token_value[1], \
                                                           token_value[2]
            if token_username:
                return jsonify(msg='该用户已经通过用户密码注册过!', code=400)
            user_from_wechatid: User = User.select_user_by_wechat_id(token_wechatid)  # 如果没有username 其实一定会有wechat
            user_from_wechatid.username = username
            user_from_wechatid.password = password
            User.add(user_from_wechatid)
            return jsonify(msg='wechat_user granted with pure register, success!', code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


@user.route("/login", methods=['POST'])
def user_login():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("pwd", "").strip()
        token = request.cookies.get("cookies", "").strip()
        user: User = User.select_user_by_username(username)
        if not user:
            return jsonify(msg='no such username', code=4000)
        if not User.check_password(user.password, password):
            return jsonify(msg='password error!', code=4000)
        token_delivered = Token(user.id, user.username, user.wechatid).deliver_token()
        print(token_delivered)
        resp = make_response(jsonify(msg='login via pure, success!', code=200))
        resp.set_cookie("cookies", token_delivered)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 用户登录通过微信，只能是新用户
@user.route("/login/wechat", methods=['GET'])
def user_wechat_login():
    code = request.args.get("code", "").strip()
    token = request.cookies.get("cookies", "").strip()
    try:
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                    "appid={:s}&" \
                    "secret={:s}&" \
                    "code={:s}&" \
                    "grant_type={:s}".format(app_id, secret, code, "authorization_code")
        res_data = json.loads(requests.get(token_url).text)
        wechatid = res_data['unionid']
        if WeUserToken.query.filter_by(unionid=res_data['unionid']).all():
            return jsonify(msg="alreay granted via wechat", code=4000)
        we_user_token = WeUserToken(openid=res_data['openid'], access_token=res_data['access_token'],
                                    refresh_token=res_data['refresh_token'], unionid=res_data['unionid'])
        db.session.add(we_user_token)
        db.session.commit()
        info_data = get_we_user_info(we_user_token)
        we_user_info = WeUserInfo(**info_data)
        db.session.add(we_user_info)
        db.session.commit()
        user = User(wechatid=wechatid)
        User.add(user)
        resp = make_response(jsonify(msg='login with wechat!', code=200))
        new_token = Token(user.id, user.username, user.wechatid).deliver_token()
        resp.set_cookie("cookies", new_token)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 用户授权，已经有Pure的用户
@user.route("/grant/wechat", methods=['GET'])
def user_wechat_grant():
    code = request.args.get("code", "").strip()
    token = request.cookies.get("cookies", "").strip()
    try:
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]

        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                    "appid={:s}&" \
                    "secret={:s}&" \
                    "code={:s}&" \
                    "grant_type={:s}".format(app_id, secret, code, "authorization_code")
        res_data = json.loads(requests.get(token_url).text)
        wechatid = res_data['unionid']
        if WeUserToken.query.filter_by(unionid=res_data['unionid']).all():
            return jsonify(msg="alreay granted via wechat", code=4000)

        user: User = User.select_user_by_username(token_user_id)
        user.wechatid = wechatid
        User.add(user)
        resp = make_response(jsonify(msg='grand pure user with wechat!', code=200))
        new_token = Token(user.id, user.username, user.wechatid).deliver_token()
        resp.set_cookie("cookies", new_token)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


@user.route("/logout", methods=['GET'])
def user_logout():
    try:
        userID = request.args.get("userID", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_user_id = Token.get_token_value(token)[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        Token.delete_token(token)
        resp = make_response(jsonify(msg="user logout, success!", code=200))
        resp.set_cookie("cookies", "")
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg="kernel error", code=4000)


# 获取用户信息
@user.route("/get/info", methods=['GET'])
def user_get_info():
    try:
        userID = request.args.get("userID", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_user_id = Token.get_token_value(token)[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user = User.select_user_by_id(userID)
        data = user.get_specific_info("username", "nickname", "avatar",
                                      "gender", "city", "job", "age", "province",
                                      "country")
        resp = make_response(jsonify(msg="get user info, success", code=200, data=
        data))
        resp.set_cookie("cookies", token)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg="kernel error", code=4000)


# 基本信息修改
@user.route("/update/info/", methods=['POST'])
def user_info_update():
    try:
        request_json = request.get_json()
        userID = request_json['userID']
        gender = request_json['gender']
        city = request_json['city']
        country = request_json['country']
        province = request_json['province']
        job = request_json['job']
        nickname = request_json['nickname']
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_user_id = Token.get_token_value(token)[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user: User = User.select_user_by_id(userID)
        user.gender = gender
        user.city = city
        user.country = country
        user.province = province
        user.job = job
        user.nickname = nickname
        User.add(user)
        return jsonify(msg="update info, success", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 改头像
@user.route("/update/avatar/", methods=['POST'])
def user_avatar_update():
    try:
        userID = request.json.get("userID", '').strip()
        avatar = request.json.get("userID", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_user_id = Token.get_token_value(token)[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user: User = User.select_user_by_id(userID)
        user.avatar = avatar
        User.add(user)
        return jsonify(msg="update avatar, success", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 修改密码
@user.route("/update/pwd/", methods=['POST'])
def user_pwd_update():
    try:
        userID = request.json.get("userID", '').strip()
        old_pwd = request.json.get("oldpwd", '').strip()
        new_pwd = request.json.get("newpwd", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_user_id = Token.get_token_value(token)[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user: User = User.select_user_by_id(userID)
        if not User.check_password(user.password, old_pwd):
            return jsonify(msg="old password error!", code=4000)
        user.password = new_pwd
        User.add(user)
        return jsonify(msg="update password, success", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 搜索接口
@user.route("/search", methods=['GET'])
def user_search_news():
    """
    return: 新闻在数据库中的id  默认10条  列表形式
    """
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    input = request.args.get("input", "").strip()
    if not isinstance(re, dict):
        return re
    user_id = re['id']
    try:
        # search_result = es.search(input)
        # return Success(data={'id_list': search_result})
        return Success(data={'id_list': 'search_result'})
    except Exception as e:
        print(e)
        return ERROR(msg="搜索失败")


@user.route("/wechat/userinfo", methods=['GET'])
def get_we_user_info():
    unionid = request.args.get('unionid', "").strip()
    if unionid:
        try:
            pass
        except Exception as e:
            print(e)
            return jsonify(mgs="数据库操作有错", code=4001)
    else:
        return jsonify(msg="未收到unionid", code=4000)


# test just for
@user.route("/wechat/test", methods=['GET'])
def test():
    user_kwargs = "openid", "code", "access", "refresh", "unionid"
    we_user_token = WeUserToken(openid="openid", code="code", access_token="access", refresh_token="refresh",
                                unionid="unionid")
    db.session.add(we_user_token)
    db.session.commit()
    return jsonify(msg="未收到code", code=4000)
