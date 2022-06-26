# -*- coding:utf-8 -*-
import requests
import json
import time
import math
import hashlib

def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS,CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    print("AS:"+AS,"CP:"+CP)
    return AS,CP



def get_url(max_behot_time,AS,CP):
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1' \
           '&max_behot_time={0}' \
           '&max_behot_time_tmp={0}' \
           '&tadrequire=true' \
           '&as={1}' \
           '&cp={2}'.format(max_behot_time,AS,CP)
    print(url)
    return url

def get_item(url):
    cookies = {"tt_webid":"6413971664988276225"}
    head = {
        "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
        "cookie": r"msToken=E36K5JHB6DJ9HGvaPn2VfYWeqsYfTsOIRH1baNpbONA-RhXdAOUEwgzPRo8punfgy6-dxXwrtu33HzAHknXLIN1BPcI9jw49wojerBNoN9Ee; __ac_signature=_02B4Z6wo00f0150YAowAAIDC.hLC5g2uFI-dOAYAAIX940; tt_webid=7083040993302414885; ttcid=0866514bfa7e467d8b605337ba6e566f40; local_city_cache=%E5%90%89%E5%AE%89; _tea_utm_cache_24=undefined; csrftoken=2dbceb7291f033fbba7e0a8dccfab318; s_v_web_id=verify_l4pov1ed_w3G5ES6c_qfeq_4O0q_BuHa_OMfXqOScF3mP; _tea_utm_cache_1300=undefined; ttwid=1%7CY_eti32yaL9AfkPRtjeQ6StsIbxvlmmTL2R2kaaWpbs%7C1655912042%7C7ab1fb744827f21814fb82a43849c5ed1ed485312b6746c6b4eb01dba90bdd54; MONITOR_WEB_ID=075c333f-0f89-4e2e-9ee0-538e5d760cf0; tt_scid=LY5OWvFahHL7Acr1.XsPBmjI-BPPa5T2tnbaWl-A0YhkFfUxulhfOh4rksJVo41qb185",
        'referer': 'https://www.toutiao.com/',
        'origin': 'https://www.toutiao.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0'
    }
    wbdata = requests.get(url,headers=head).content
    wbdata2 = json.loads(wbdata)

    data = wbdata2['data']
    for news in data:
        title = news['title']
        news_url = news['source_url']
        news_url = "https://www.toutiao.com"+news_url

        print(title,news_url)
    print(wbdata2)
    next_data = wbdata2['next']
    next_max_behot_time = next_data['max_behot_time']
    print("next_max_behot_time:{0}".format(next_max_behot_time))
    return next_max_behot_time


refresh = 50
for x in range(0,refresh+1):
    print("第{0}次：".format(x))
    if x == 0:
        max_behot_time = 0
    else:
        max_behot_time = next_max_behot_time
        print (max_behot_time)

    AS,CP = getASCP()
    url = get_url(max_behot_time,AS,CP)
    next_max_behot_time = get_item(url)