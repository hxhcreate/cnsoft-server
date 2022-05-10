import time
import datetime
import requests
import json

from flask import request, jsonify, session

from . import user
from ..models import User, db, WeUserToken
from ..tools.decoration import login_required

from ..config import app_id, secret
from ..config.redis import redis_db
from ..tools.auth import Auth

from ..tools.message import *


@user.route("/register", methods=['POST'])
def user_register():
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    sign = request.json.get("sign", "").strip()
    if not all([username, password]):
        return jsonify(msg='用户和密码不能为空', code=403)
    if User.is_exist_user_by_username(username):
        return jsonify(msg='用户名重复', code=403)
    try:
        user = User(username=username, password=password)
        User.add(user)
        return jsonify(msg="注册成功", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg="数据库操作有错", code=402)


@user.route("/login", methods=['POST'])
def user_login():
    username = request.json.get("username", "").strip()
    ori_password = request.json.get("password", "").strip()
    sign = request.json.get("sign", "").strip()

    if not all([username, ori_password]):
        return jsonify(msg='用户和密码不能为空', code=403)
    user = User.select_user_by_username(username)
    if isinstance(user, None):
        return jsonify(msg='未查找到该用户', code=402)

    # 引入Auth板块
    if Auth.authenticate(ori_password, user.password):
        time_stamp = int(time.time())
        token = Auth.encode_auth_token(user.id, time_stamp, "pure", user.type)
        redis_db.handle_redis_token("user" + str(user.id), token)
        return Success(
            {"token": token, "logtime": time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime(time_stamp)),
             "username": user.username, "id": user.id})
    else:
        return jsonify(msg='账号或者密码错误', code=403)


@user.route("/logout", methods=['DELETE'])
def user_logout():
    id = request.args.get("userID", "").strip()
    if id:
        key = "user" + str(id)
        if session.get(key) is not None:
            session.pop(key)
            return jsonify(msg="用户退出登录成功", code=200)
        else:
            return jsonify(msg='用户尚未登录', code=403)
        # if redis_db.exists_key(key):
        #     redis_db.del_key(key)
        #     return jsonify(msg="用户退出登录成功", code=200)
        # else:
        #     return jsonify(msg='用户尚未登录', code=403)
    return jsonify(msg='用户ID不能为空', code=403)


# 检查登录状态
@user.route("/session/<int:id>", methods=['GET'])
def user_check_session(id):
    if redis_db.exists_key("user" + str(id)):
        return jsonify(id=id, code=200)
    else:
        return jsonify(msg="用户尚未登录", code=403)


# 获取用户信息
@user.route("/get/info", methods=['GET'])
def user_get_info():
    auth_header = request.headers.get('Authorization')
    id = request.args.get("id", "").strip()
    sign = request.args.get("sign", "").strip()
    re = Auth.identify(auth_header)  # 正确就是字典  不正确就是一个jsonify
    if not isinstance(re, dict):
        return re
    if id == re['id']:
        user = User.select_user_by_id(id)
        if user is None:
            return jsonify(msg='未查找到该用户', code=402)
        result = {"id": user.id, "cate": user.cate,
                  "username": user.username, "nickname": user.nickname,
                  "avatar": user.avatar, "gender": user.gender,
                  "city": user.city, "job": user.job,
                  "age": user.age}
        return jsonify(code=200, msg='获取用户信息成功', data=result)
    else:
        return jsonify(msg='该用户只能修改自己的用户信息', code=403)


# 获取用户平台信息
@user.route("/get/info/detail", methods=['GET'])
def user_get_stats_info():
    id = request.args.get("id", "").strip()
    sign = request.args.get("sign", "").strip()
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    if not isinstance(re, dict):
        return re
    if id == re['id']:
        user = User.select_user_by_id(id)
        if user is None:
            return jsonify(msg='未查找到该用户', code=402)
        result = {"id": user.id, "phone": user.phone,
                  "wechatID": user.wechat_id, "exp": user.exp,
                  "level": user.level, "regTime": user.reg_time,
                  "days": (datetime.datetime.now() - user.reg_time).days}
        return jsonify(code=200, msg='获取用户平台信息成功', data=result)
    else:
        return jsonify(msg='该用户只能获取自己的信息', code=403)


# 基本信息修改
@user.route("/update/info/", methods=['POST'])
def user_info_update():
    id = request.json.get("id", "").strip()
    sign = request.json.get("sign", "").strip()
    info_dict = request.get_json()
    info_dict.pop("sign")
    info_dict.pop('id')
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    if not isinstance(re, dict):
        return re
    if re['id'] == id:
        user = User.select_user_by_id(id)
        if user is None:
            return jsonify(msg='未查找到该用户', code=402)
        try:
            user.update_user_info(info_dict)
            return jsonify(msg="修改基本成功", code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="数据库修改有错", code=402)
    return ERROR(msg='该用户只能修改自己的信息')


# 改头像
@user.route("/update/avatar/", methods=['POST'])
def user_avatar_update():
    new_avatar_url = request.json.get("avatar", "").strip()
    id = request.json.get("id", "").strip()
    sign = request.json.get("sign", "").strip()
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    if not isinstance(re, dict):
        return re
    if id == re['id']:
        try:
            user_num = User.query.filter_by(id=id).first().update({"avatar": new_avatar_url})
            db.session.commit()
            return jsonify(msg="修改用户头像成功", code=200, data={"id": user.id})
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=402)
    return ERROR(msg="该用户只能修改自己的头像")


# 修改密码
@user.route("/update/pwd/", methods=['POST'])
def user_pwd_update():
    id = request.json.get("id", "").strip()
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    if not isinstance(re, dict):
        return re
    if id == re['id']:
        old_pwd = request.json.get('oldpwd', "").strip()
        new_pwd = request.json.get('newpad', "").strip()
        sign = request.args.get("sign", "").strip()
        try:
            user = User.query.filter_by(id=id).first()
            if old_pwd == user.password:
                user.password = new_pwd
                db.session.add(user)
                db.session.commit()
                return jsonify(msg='成功', code=200, data={"id": user.id})
            else:
                return jsonify(msg='密码错误', code=403)
        except Exception as e:
            print(e)
            return jsonify(msg='数据库操作有错', code=402)
    return ERROR(msg='该用户只能修改自己的密码')


# 接入微信  暂时不使用
@user.route("/wechat", methods=['POST'])
def user_wechat_api():
    code = request.json.get("code", "").strip()
    if code:
        try:
            token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                        "appid={:s}&" \
                        "secret={:s}&" \
                        "code={:s}&" \
                        "grant_type={:s}".format(app_id, secret, code, "authorization_code")
            res_data = json.loads(requests.get(token_url).text)
            user_kwargs = res_data['openid'], code, res_data["access_token"], res_data["refresh_token"]
            user_token = WeUserToken(*user_kwargs)
            db.session.add(user_token)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(mgs="数据库操作有错", code=4001)
    else:
        return jsonify(msg="未收到code", code=4000)


"""暂时只做新闻相关API  不涉及用户方面的问题"""
