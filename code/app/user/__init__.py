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
            return jsonify(message='用户名或密码不合法', code=403, data=None)
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(message="注册成功", code=200, data=None)
        except Exception as e:
            print(e)
            return jsonify(message="数据库操作有错", code=4001) #最好不要暴露过多服务端的信息给客户端，否则会方便攻击者挖漏洞
    except Exception as e:
        print(e)
        return jsonify(message="连接出错", code=4002, data=None)


@user.route("/login", methods=['POST'])
def user_login():
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    # if not all([username, password]):
    #     return jsonify(message='用户和密码不能为空', code=4000, data=None)
    if username:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            timeStamp = int(time.time())
            session["user" + username] = str(timeStamp)  # 用来和管理员表的username做区分
            userInfo = {'username': user.username, 'password': user.password, # password也要返回吗？
                        'logtime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            return jsonify(message='登录成功', code=200, data=userInfo)
        # username 为空也视作错误
    else:
        return jsonify(message='用户名或密码错误', code=403, data=None)


@user.route("/logout/<string:username>", methods=['GET'])
def user_logout(username):
    if session.get("user" + username):
        session.pop("user" + username)
        return jsonify(message="Succeed", code=200, data=None)
    else:
        return jsonify(message='用户尚未登录', code=400, data=None)


# 检查登录状态
@user.route("/session/<string:username>", methods=['GET'])
def user_check_session(username):
    data = {"login": "false"}
    if session.get('user' + username):
        data = {"login": "true"}
    return jsonify(message="检查成功", code=200, data=data)
