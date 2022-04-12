import time
from datetime import datetime

from flask import Blueprint, request, jsonify, session

from app import db
from app.models import User

"""用户操作接口"""
user = Blueprint("user", __name__)


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
