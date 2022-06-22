import json

import requests

from ..models import WeUserToken

from ..config import app_id, secret


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
