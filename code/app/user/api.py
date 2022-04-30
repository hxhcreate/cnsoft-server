import time
import datetime
import requests
import json

from flask import request, jsonify, session

from . import user
from ..models import User, News, db, WeUserToken, WeUserInfo
from ..tools.decoration import login_required

from ..config import app_id, secret


@user.route("/register", methods=['POST'])
def user_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()
        sign = request.json.get("sign", "").strip()
        if not all([username, password]):
            return jsonify(msg='用户和密码不能为空', code=403)
        old_users = User.query.filter_by(username=username).all()
        if old_users is not []:
            return jsonify(msg='用户名重复', code=403)
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            # userInfo = {'username': user.username, 'password': user.password}
            return jsonify(msg="注册成功", code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=402)
    except Exception as e:
        print(e)
        return jsonify(msg="连接出错", code=403)


@user.route("/login", methods=['POST'])
def user_login():
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    sign = request.json.get("sign", "").strip()
    print(username)
    if not all([username, password]):
        return jsonify(msg='用户和密码不能为空', code=403)
    try:
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        print(e)
        return jsonify(msg='数据库操作有误', code=402)
    if user and user.password == password:
        timeStamp = int(time.time())

        session['user' + str(user.id)] = timeStamp
        # redis_db.handle_redis_token("user" + str(user.id), timeStamp)  # 用来和管理员表的username做区分
        userInfo = {'username': user.username,
                    "id": user.id,
                    'logtime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return jsonify(msg='登录成功', code=200, data=userInfo)
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
    # if redis_db.exists_key("user" + str(id)):
    if session.get("user" + str(id)) is not None:
        return jsonify(id=id, code=200)
    else:
        return jsonify(msg="用户尚未登录", code=403)


# 获取用户信息
@user.route("/get/info", methods=['GET'])
def user_get_info():
    id = request.args.get("id", "").strip()
    sign = request.args.get("sign", "").strip()
    if id:
        try:
            user = User.query.filter_by(id=id).first()
        except Exception as e:
            print(e)
            return jsonify(msg='数据查询出错', code=402)
        if user is not None:
            result = {"id": user.id, "cate": user.cate,
                      "username": user.username, "nickname": user.nickname,
                      "avatar": user.avatar, "gender": user.gender,
                      "city": user.city, "job": user.job,
                      "age": user.age}
            return jsonify(code=200, msg='获取用户信息成功', data=result)
        else:
            return jsonify(msg='未找到该用户', code=403)
    else:
        return jsonify(msg='用户ID不能为空', code=403)


# 获取用户平台信息
@user.route("/get/info/detail", methods=['GET'])
def user_get_stats_info():
    id = request.args.get("id", "").strip()
    sign = request.args.get("sign", "").strip()
    if id:
        try:
            user = User.query.filter_by(id=id).first()
        except Exception as e:
            print(e)
            return jsonify(msg='数据库查询出错', code=403)
        if user is not None:
            result = {"id": user.id, "phone": user.phone,
                      "wechatID": user.wechat_id, "exp": user.exp,
                      "level": user.level, "regTime": user.reg_time,
                      "days": (datetime.datetime.now() - user.reg_time).days}
            return jsonify(code=200, msg='获取用户平台信息成功', data=result)
        else:
            return jsonify(msg='未查询到该用户', code=403)
    else:
        return jsonify(msg='用户ID不能为空', code=403)


# 基本信息修改

@user.route("/update/info/", methods=['GET'])
def user_info_update():
    id = request.args.get("id", "").strip()
    if session.get("user" + str(id)) is not None:
        try:
            user = User.query.filter_by(id=id).first()
        except Exception as e:
            print(e)
            return jsonify(msg='数据查询出错', code=402)
        sign = request.args.get("sign", "").strip()
        nickname = request.args.get("nickname", "").strip()
        gender = request.args.get("gender", "").strip()
        age = request.args.get("age", "").strip()
        city = request.args.get("city", "").strip()
        job = request.args.get("job", "").strip()
        if user is not None:
            try:
                user.nickname = nickname if nickname else user.nickname
                user.gender = gender if gender else user.gender
                user.age = age if age else user.age
                user.city = city if city else user.city
                user.job = job if job else user.job
                db.session.add(user)
                db.session.commit()
                return jsonify(msg="修改基本成功", code=200)
            except Exception as e:
                print(e)
                return jsonify(msg="数据库修改有错", code=402)
        else:
            return jsonify(msg="未查找到该用户，无法修改", code=403)
    return jsonify(msg='用户未登录不能修改', code=403)


# 改头像
@user.route("/update/avatar/", methods=['GET'])
def user_avatar_update():
    new_avatar_url = request.args.get("avatar", "").strip()
    id = request.args.get("id", "").strip()
    if session.get("user" + str(id)) is not None:
        sign = request.args.get("sign", "").strip()
        try:
            user_num = User.query.filter_by(id=id).first().update({"avatar": new_avatar_url})
            db.session.commit()
            return jsonify(msg="修改用户头像成功", code=200, data={"id": user.id})
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=402)
    return jsonify(msg='用户未登录不能修改', code=403)


# 修改密码
@user.route("/update/pwd/", methods=['POST'])
def user_pwd_update():
    id = request.json.get("id", "").strip()
    if session.get("user" + id) is not None:
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
    return jsonify(msg='用户未登录不能修改', code=403)


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
