import time
import datetime

from flask import request, jsonify, session

from . import user
from ..models import User, db


@user.route("/register", methods=['POST'])
def user_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()
        if not all([username, password]):
            return jsonify(msg='用户和密码不能为空', code=4000)
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            userInfo = {'username': user.username, 'password': user.password}
            return jsonify(msg="注册成功", code=200, data=userInfo)
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=4001)
    except Exception as e:
        print(e)
        return jsonify(msg="连接出错", code=4002)


@user.route("/login", methods=['POST'])
def user_login():
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    if not all([username, password]):
        return jsonify(msg='用户和密码不能为空', code=4000)
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        timeStamp = int(time.time())
        session["user" + username] = str(timeStamp)  # 用来和管理员表的username做区分
        userInfo = {'username': user.username, 'password': user.password,
                    'logtime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return jsonify(msg='登录成功', code=200, data=userInfo)
    else:
        return jsonify(msg='账号或者密码错误', code=4000)


@user.route("/logout/<string:username>", methods=['DELETE'])
def user_logout(username):
    if session.get("user" + username):
        session.pop("user" + username)
        return jsonify(msg="用户退出登录成功", code=200)
    else:
        return jsonify(msg='用户尚未登录', code=4000)


# 检查登录状态
@user.route("/session/<string:username>", methods=['GET'])
def user_check_session(username):
    if session.get('user' + username) is not None:
        return jsonify(username=username, code=200)
    else:
        return jsonify(msg="用户尚未登录", code=4000)


# 基本信息修改
@user.route("/update/info/<string:username>", methods=['PUT'])
def user_info_update(username):
    nickname = request.json.get("nickname", "").strip()
    gender = request.json.get("gender", "").strip()
    age = request.json.get("age", "").strip()
    address = request.json.get("address", "").strip()
    job = request.json.get("job", "").strip()
    user = User.query.filter_by(username=username).first()
    if user is not None:
        try:
            user.nickname = nickname
            user.gender = gender
            user.age = age
            user.address = address
            user.job = job
            db.session.add(user)
            db.session.commit()
            return jsonify(msg="修改基本成功", code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=4001)
    else:
        return jsonify(msg="未查找到该用户，无法修改", code=4000)


# 改头像
@user.route("/update/avatar/<string:username>", methods=['PUT'])
def user_avatar_update(username):
    new_avatar_url = request.json.get("avatar", "").strip()
    try:
        user_num = User.query.filter_by(username=username).first().update({"avatar": new_avatar_url})
        db.session.commit()
        return jsonify(msg="修改用户头像成功", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg="数据库操作有错", code=4001)

