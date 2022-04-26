import time
from datetime import datetime

from flask import request, jsonify, session

from . import admin
from ..models import Admin, db





"""管理员接口"""

@admin.route("/", methods=['GET'])
def admin_index():
    return "This is index page."

@admin.route("/register", methods=['POST'])
def admin_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()
        if not all([username, password]):
            return jsonify(msg='管理员和密码不能为空', code=4000)
        admin = Admin(username=username, password=password)
        try:
            db.session.add(admin)
            db.session.commit()
            userInfo = {'username': admin.username, 'password': admin.password}
            return jsonify(msg="管理员注册成功", code=200, data=userInfo)
        except Exception as e:
            print(e)
            return jsonify(msg="数据库操作有错", code=4001)
    except Exception as e:
        print(e)
        return jsonify(msg="连接出错", code=4002)


@admin.route("/login", methods=['POST'])
def admin_login():
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    if not all([username, password]):
        return jsonify(msg='管理员名和密码不能为空', code=4000)
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.password == password:
        timeStamp = int(time.time())
        session["admin" + username] = str(timeStamp)
        userInfo = {'username': admin.username, 'password': admin.password,
                    'logtime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return jsonify(msg='管理员登录成功', code=200, data=userInfo)
    else:
        return jsonify(msg='账号或者密码错误', code=4000)


@admin.route("/logout/<string:username>", methods=['DELETE'])
def admin_logout(username):
    if session.get("admin" + username):
        session.pop("admin" + username)
        return jsonify(msg="管理员退出登录成功", code=200)
    else:
        return jsonify(msg='管理员尚未登录', code=4000)


# 检查登录状态
@admin.route("/session/<string:username>", methods=['GET'])
def admin_check_session(username):
    if session.get("admin" + username) is not None:
        return jsonify(username=username, code=200)
    else:
        return jsonify(msg="管理员尚未登录", code=4000)

