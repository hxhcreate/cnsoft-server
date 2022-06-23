import time
import datetime
import requests
import json

from flask import request, jsonify, session

from . import user
from ..models import User, db, WeUserToken, create_user, WeUserInfo
from .wechat import *
from ..tools.decoration import login_required

from ..config import app_id, secret
from ..config.redis import redis_db
from ..tools.auth import Auth
# from ..config.es import es

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
        create_user(username, password)
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
    if user is None:
        return jsonify(msg='未查找到该用户', code=402)

    if Auth.authenticate(ori_password, user.password):
        time_stamp = int(time.time())
        token = Auth.encode_auth_token(user.id, time_stamp)
        print(token)
        redis_db.handle_redis_token("user" + str(user.id), token)
        return Success(
            {"token": token, "logtime": time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime(time_stamp)),
             "username": user.username, "id": user.id})
    else:
        return jsonify(msg='账号或者密码错误', code=403)


@user.route('/login/grant', methods=['GET'])
def user_grant():
    userid = request.json.get('userid', '').strip()
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    if userid and username and password:
        user = User.select_user_by_id(userid)
        user.username = username
        user.password = password
        User.add(user)
        return jsonify(msg="用户密码设置成功", status=200)
    else:
        return jsonify(msg="参数不全", status=4000)


# 接入获取微信授权
# 根据参数判断是授权还是注册
@user.route("/login/wechat", methods=['GET'])
def user_wechat_login():
    code = request.args.get("code", "").strip()
    auth_header = request.headers.get('Authorization').strip()
    user_id = request.args.get("userid", "").strip()
    if code:
        try:
            token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                        "appid={:s}&" \
                        "secret={:s}&" \
                        "code={:s}&" \
                        "grant_type={:s}".format(app_id, secret, code, "authorization_code")
            res_data = json.loads(requests.get(token_url).text)
            # 判断用户是否在另一个平台已经注册过了
            # 已经授权过，则不再获取token等
            if not WeUserToken.query.filter_by(unionid=res_data['unionid']).all():
                we_user_token = WeUserToken(openid=res_data['openid'], access_token=res_data['access_token'],
                                            refresh_token=res_data['refresh_token'], unionid=res_data['unionid'])
                db.session.add(we_user_token)
                db.session.commit()
                info_data = get_we_user_info(we_user_token)
                we_user_info = WeUserInfo(**info_data)
                db.session.add(we_user_info)
                db.session.commit()
                print("we_user创建完成")
                if auth_header and user_id:
                    re = Auth.identify(auth_header)  # 正确就是字典  不正确就是一个jsonify
                    if not isinstance(re, dict):
                        return re
                    print("鉴权成功")
                    user = User.select_user_by_id(user_id)
                    user.wechat_id = res_data['unionid']
                    user.gender = we_user_info['sex']
                    user.city = we_user_info['city']
                    user.province = we_user_info['province']
                    user.country = we_user_info['country']
                    user.avatar = we_user_info['headimgurl']
                    user.nickname = we_user_info['nickname']
                    User.add(user)
                    return jsonify(msg="通过wechat授权user成功", code=200, data={'userid': user.id})
                else:
                    user = User(wechat_id=res_data['unionid'])  # 创建新的用户
                    time_stamp = int(time.time())
                    token = Auth.encode_auth_token(user.id, time_stamp)
                    print(token)
                    redis_db.handle_redis_token("user" + str(user.id), token)
                    user = User.select_user_by_id(user_id)
                    user.wechat_id = res_data['unionid']
                    user.gender = we_user_info['sex']
                    user.city = we_user_info['city']
                    user.province = we_user_info['province']
                    user.country = we_user_info['country']
                    user.avatar = we_user_info['headimgurl']
                    user.nickname = we_user_info['nickname']
                    User.add(user)
                    return jsonify(msg="通过wechat创建新的user", code=200, data={'userid': user.id,
                                                                           "token": token})
            else:
                return jsonify(msg="we_user已经授权过", code=200, data={'unionid': res_data['unionid']})
        except Exception as e:
            print(e)
            return jsonify(mgs="数据库操作有错", code=4001)
    else:
        return jsonify(msg="未收到code", code=4000)


# @user.route("/grant/wechat", methods=['GET'])
# def user_wechat_grant():
#     code = request.args.get("code", "").strip()
#     auth_header = request.headers.get('Authorization').strip()
#     user_id = request.args.get("userid", "").strip()
#     if auth_header and user_id:
#         wechat_grant(code)
#     else:
#         return jsonify(msg="授权请提供token和id", status=4000)


@user.route("/login/miniprogram", methods=['GET'])
def user_miniprogram_login():
    return


@user.route("/logout", methods=['DELETE'])
def user_logout():
    """
    两种角色  id也可以是admin表和user表
    """
    auth_header = request.headers.get('Authorization')
    id = request.args.get("id", "").strip()
    type = request.args.get("type", "").strip()
    sign = request.args.get("sign", "").strip()
    re = Auth.identify(auth_header)  # 正确就是字典  不正确就是一个jsonify
    if not isinstance(re, dict):
        return re
    if re['type'] == '0':
        if type != '0':
            redis_db.del_key("user" + str(id))
            return Success(msg="管理员操作用户退出成功")
        else:
            if id == re['id']:
                redis_db.del_key("admin" + str(id))
                return Success(msg='管理员退出登录成功')
            return ERROR(msg='该管理员只能退出自己的账号')
    else:
        if type == '0':
            return ERROR("用户不能操作管理员账户")
        else:
            if re['id'] == id:
                redis_db.del_key("user" + str(id))
                return Success(msg='用户退出登录成功')
            return ERROR(msg="该用户只能操作自己退出登录")


# 获取用户信息
@user.route("/get/info", methods=['GET'])
def user_get_info():
    auth_header = request.headers.get('Authorization')
    id = request.args.get("id", "").strip()
    sign = request.args.get("sign", "").strip()
    re = Auth.identify(auth_header)  # 正确就是字典  不正确就是一个jsonify
    if not isinstance(re, dict):
        return re
    if re['type'] == "0" or id == re['id']:
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
    if re['type'] == "0" or id == re['id']:
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
    if re['type'] == "0" or re['id'] == id:
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
    """
    fdsaf
    """
    new_avatar_url = request.json.get("avatar", "").strip()
    id = request.json.get("id", "").strip()
    sign = request.json.get("sign", "").strip()
    auth_header = request.headers.get('Authorization')
    re = Auth.identify(auth_header)
    if not isinstance(re, dict):
        return re
    if re['type'] == "0" or id == re['id']:
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
    if re['type'] == '0' or id == re['id']:
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
