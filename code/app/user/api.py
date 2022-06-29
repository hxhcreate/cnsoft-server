from ..tools.auth import Auth

from ..tools.message import *

# 用户管理api
from .user_manage import *

from ..config import SESSION_EXPIRE_TIME


@user.route("/logout", methods=['GET'])
def user_logout():
    try:
        userID = int(request.args.get("userID", '').strip())
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        Token.delete_token(token)
        resp = make_response(jsonify(msg="user logout, success!", code=200))
        resp.set_cookie("cookies", "", max_age=SESSION_EXPIRE_TIME)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg="kernel error", code=4000)


# 获取用户信息
@user.route("/get/info", methods=['GET'])
def user_get_info():
    try:
        userID = int(request.args.get("userID", '').strip())
        print(userID)
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user = User.select_user_by_id(userID)
        data = user.get_specific_info("username", "nickname", "avatar",
                                      "gender", "city", "job", "age", "province",
                                      "country")

        resp = make_response(jsonify(msg="get user info, success", code=200, data=data))
        resp.set_cookie("cookies", token, max_age=SESSION_EXPIRE_TIME)
        resp.status = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(msg="kernel error", code=4000)


# 基本信息修改
@user.route("/update/info", methods=['POST'])
def user_info_update():
    try:
        request_json = request.get_json()
        userID = int(request_json['userID'])
        gender = int(request_json['gender'])
        city = request_json['city']
        country = request_json['country']
        province = request_json['province']
        job = request_json['job']
        nickname = request_json['nickname']
        age = request_json['age']
        token = request.cookies.get("cookies", "").strip()
        print("get token: %s" % token)
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user: User = User.select_user_by_id(userID)
        user.gender = gender
        user.city = city
        user.country = country
        user.province = province
        user.job = job
        user.nickname = nickname
        user.age = age
        User.add(user)
        return jsonify(msg="update info, success", code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 改头像
@user.route("/update/avatar", methods=['POST'])
def user_avatar_update():
    try:
        userID = int(request.json.get("userID", '').strip())
        avatar = request.json.get("avatar", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
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
@user.route("/update/pwd", methods=['POST'])
def user_pwd_update():
    try:
        userID = int(request.json.get("userID", '').strip())
        old_pwd = request.json.get("oldpwd", '').strip()
        new_pwd = request.json.get("newpwd", '').strip()
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
        if userID != int(token_user_id):
            return jsonify(msg="token is not valid for this operation", code=4000)

        user: User = User.select_user_by_id(userID)
        print(user.password)
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


# test just for
@user.route("/wechat/test", methods=['GET'])
def test():
    user_kwargs = "openid", "code", "access", "refresh", "unionid"
    we_user_token = WeUserToken(openid="openid", code="code", access_token="access", refresh_token="refresh",
                                unionid="unionid")
    db.session.add(we_user_token)
    db.session.commit()
    return jsonify(msg="未收到code", code=4000)
