import time
from datetime import datetime
import base64

from flask import Flask, request, jsonify, session, url_for, render_template, send_from_directory, Response

from . import admin
from ..models import Admin, db
from random import randrange

from pyecharts import options as opts
from pyecharts.charts import Bar
from .gen_graph import gender_pie, age_bar, city_bar, news_click_rate, news_collection, user_numAndIncrease

"""管理员接口"""


@admin.route("/", methods=['GET'])
def admin_index():
    return render_template("index.html")

@admin.route("/index.css", methods=['GET'])
def admin_css():
    return render_template("index.css")

@admin.route("/icon/icon.png", methods=['GET'])
def admin_icon():
    return Response(open("app/admin/templates/ico/透明底（如有需要）PNG1024px,300dpi.png", 'rb').read(), mimetype="img/png")
    
@admin.route("/get_gender_pie")
def get_gender_pie():
    c = gender_pie().dump_options()
    return c


@admin.route("/get_age_bar")
def get_age_bar():
    c = age_bar().dump_options()
    return c


@admin.route("/get_city_bar")
def get_city_bar():
    c = city_bar().dump_options_with_quotes()
    return c


@admin.route("/get_news_click_rate")
def get_news_click_rate():
    c = news_click_rate().dump_options()
    return c


@admin.route("/get_news_collection")
def get_news_collection():
    c = news_collection().dump_options()
    return c


@admin.route("/get_user_numAndIncrease")
def get_user_numAndIncrease():
    c = user_numAndIncrease().dump_options()
    return c


# 用新方案，没有登录系统的话，以下都没用
'''
@admin.route("/register", methods=['POST'])
def admin_register():
    try:
        # dataJson = request.form.to_dict()
        dataJson = request.json
        username = dataJson.get("username", "").strip()
        password = dataJson.get("password", "").strip()
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
    # dataJson = request.form.to_dict()
    dataJson = request.json
    print(dataJson)
    username = dataJson.get("username", "").strip()
    password = dataJson.get("password", "").strip()
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


@admin.route("/code", methods=['GET'])
def admin_code():
    # img = base64.encodebytes(open(r'D:\@project\2022-3cnsoft\server\code\dist\favicon.ico', 'rb').read()).decode()
    # return jsonify(img=img, uuid='hhh')
    return '{"uuid":"code-key-34139e2a1c1c47fb99c193b8778fc058","img":"data:image/png;base64,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"}'


@admin.route("/static/<path:path>", methods=['GET'])
def admin_static(path):
    return send_from_directory('../dist/static/' + '/'.join(path.split('/')[0:-1]), path.split('/')[-1])

'''
