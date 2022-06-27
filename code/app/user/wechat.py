import json

import requests

from ..models import WeUserToken, db, WeUserInfo

from ..config import app_id, secret

from flask import jsonify


def refresh_token(we_user_token: WeUserToken):
    # 判断失效才获取
    valid_url = 'https://api.weixin.qq.com/sns/auth?' \
                'access_token=%s&' \
                'openid=%s' % (we_user_token.access_token, we_user_token.openid)
    if not json.loads(requests.get(valid_url).text)['errcode']:
        refresh_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?' \
                      'appid=%s&' \
                      'grant_type=refresh_token&' \
                      'refresh_token=%s' % (app_id, we_user_token.refresh_token)
        res_data = json.loads(requests.get(refresh_url).text)
        we_user_token.access_token = res_data['access_token']
        we_user_token.refresh_token = res_data['refresh_token']


def get_we_user_info(we_user_token: WeUserToken):
    info_url = 'https://api.weixin.qq.com/sns/userinfo?' \
               'access_token=%s&' \
               'openid=%s&' \
               'lang=zh_CN' % (we_user_token.access_token, we_user_token.openid)
    res_data = json.loads(requests.get(info_url).text)
    return res_data


def wechat_grant(code):
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
                return jsonify(msg="创建新we_user", code=200, data={'unionid': res_data['unionid']})
            else:
                return jsonify(msg="we_user已经授权", code=200, data={'unionid': res_data['unionid']})
        except Exception as e:
            print(e)
            return jsonify(mgs="数据库操作有错", code=4001)
    else:
        return jsonify(msg="未收到code", code=4000)
