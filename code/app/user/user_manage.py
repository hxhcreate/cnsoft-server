import requests
from flask import request, jsonify, session, make_response
from . import user
from .wechat import get_we_user_info
from ..config import app_id, secret

from ..models import User, db, WeUserToken, WeUserInfo, create_user
from ..tools.token import Token
import json


@user.route("/register", methods=['POST'])
def user_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("pwd", "").strip()
        token = request.cookies.get("cookies", "").strip()
        if User.is_exist_user_by_username(username):
            return jsonify(msg='duplicate username, failed!', code=400)
        if token is "":  # 不携带token
            create_user(username=username, password=password)
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
<<<<<<< HEAD
        resp = make_response(jsonify(msg='login via pure, success!', code=200, data={'userID': user.id}))
=======
        resp = make_response(jsonify(msg='login via pure, success!', code=200))
>>>>>>> 1c58585d8e797f2c933084a61bfa954cf5c344c4
        resp.set_cookie("cookies", token_delivered)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 用户登录通过微信，只能是新用户
@user.route("/login/wechat", methods=['GET'])
def user_wechat_login():
    try:
        code = request.args.get("code", "").strip()
        token = request.cookies.get("cookies", "").strip()
        userID = int(request.args.get("userID", ""))
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                    "appid={:s}&" \
                    "secret={:s}&" \
                    "code={:s}&" \
                    "grant_type={:s}".format(app_id, secret, code, "authorization_code")
        res_data = json.loads(requests.get(token_url).text)
        wechatid = res_data['unionid']
        if WeUserToken.query.filter_by(unionid=res_data['unionid']).all():
            return jsonify(msg="alreay granted via wechat", code=4000)

        if int(userID) == -1:  # new user
            we_user_token = WeUserToken(openid=res_data['openid'], access_token=res_data['access_token'],
                                        refresh_token=res_data['refresh_token'], unionid=res_data['unionid'])
            db.session.add(we_user_token)
            db.session.commit()
            info_data = get_we_user_info(we_user_token)
            we_user_info = WeUserInfo(**info_data)
            db.session.add(we_user_info)
            db.session.commit()
            user = create_user(wechatid=wechatid)
            resp = make_response(jsonify(msg='login with wechat!', code=200))
            new_token = Token(user.id, user.username, user.wechatid).deliver_token()
            resp.set_cookie("cookies", new_token)
            resp.status = 200
            return resp
        else:
            userID = int(userID)
            user: User = User.select_user_by_id(userID)
            user.wechatid = wechatid
            User.add(user)
            resp = make_response(jsonify(msg='grant pure user with wechat!', code=200))
            new_token = Token(user.id, user.username, user.wechatid).deliver_token()
            resp.set_cookie("cookies", new_token)
            resp.status = 200
            return resp
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)
