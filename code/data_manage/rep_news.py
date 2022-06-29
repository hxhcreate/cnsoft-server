import requests

requests.packages.urllib3.disable_warnings()
import json
import re
import sys

import pandas as pd

sys.path.append('..')
from app.cloudAPI.Signature import get_fullurl
from app import db  # 引入的是manage中已经实例化app的db
from app import create_app
from app.models import News

app = create_app("develop")  # 生产环境


def get_news_list():
    try:
        response = json.loads(requests.get("https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc").text).get(
            "data", [])
        news = []
        for i in response:
            news.append(i)
        return news
    except:
        return []


def parse_news(news: list):
    parsed_news = []
    head = {
        "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
        "cookie": r"msToken=E36K5JHB6DJ9HGvaPn2VfYWeqsYfTsOIRH1baNpbONA-RhXdAOUEwgzPRo8punfgy6-dxXwrtu33HzAHknXLIN1BPcI9jw49wojerBNoN9Ee; __ac_signature=_02B4Z6wo00f0150YAowAAIDC.hLC5g2uFI-dOAYAAIX940; tt_webid=7083040993302414885; ttcid=0866514bfa7e467d8b605337ba6e566f40; local_city_cache=%E5%90%89%E5%AE%89; _tea_utm_cache_24=undefined; csrftoken=2dbceb7291f033fbba7e0a8dccfab318; s_v_web_id=verify_l4pov1ed_w3G5ES6c_qfeq_4O0q_BuHa_OMfXqOScF3mP; _tea_utm_cache_1300=undefined; ttwid=1%7CY_eti32yaL9AfkPRtjeQ6StsIbxvlmmTL2R2kaaWpbs%7C1655912042%7C7ab1fb744827f21814fb82a43849c5ed1ed485312b6746c6b4eb01dba90bdd54; MONITOR_WEB_ID=075c333f-0f89-4e2e-9ee0-538e5d760cf0; tt_scid=LY5OWvFahHL7Acr1.XsPBmjI-BPPa5T2tnbaWl-A0YhkFfUxulhfOh4rksJVo41qb185",
        'referer': 'https://www.toutiao.com/',
        'origin': 'https://www.toutiao.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0'
    }
    for i in news:
        url = i.get("Url", "")
        if url:
            try:
                html = requests.get(url, headers=head, timeout=1).text
            except:
                continue
            text = re.findall(r'<div class="abstract-container ">[\s\S]*?<p class="abstract-text">([\s\S]*?)</p>', html)
            # print(text)
            if text:
                parsed_news.append({
                    "title": i.get("Title", ""),
                    "text": text[0]
                })
            # break
    return parsed_news


column_field = ["ID", "title", "text", 'class_level1', 'class_level2', 'keywords']


def request_class(news: list):
    csv = pd.DataFrame(columns=column_field)
    for index, i in enumerate(news):
        news_row = pd.Series([str(index), i['title'], i['text'], None, None, None], index=column_field)
        csv = pd.concat([csv, news_row.to_frame().T], ignore_index=True)
    url = '/api/nlp/v1/industry'
    fullurl = get_fullurl('POST', url)
    body = {"items": []}
    num = 0
    while not num == len(csv):
        for i in csv.itertuples():
            num += 1
            if 0 < len(getattr(i, 'text')) < 4096 and num % 20 != 0:
                body['items'].append({
                    "textId": getattr(i, 'ID'),
                    "title": getattr(i, 'title'),
                    "content": getattr(i, 'text')
                })
        response = requests.post(fullurl, data=json.dumps(body),
                                 headers={"Content-Type": "application/json"},
                                 timeout=(5, 60),
                                 verify=False)
        if response.json().get('state', '') == 'OK':
            for item in response.json().get('body', {}).get('items', []):
                class_level1 = item['industries'][0]['labelName'] if item['industries'] else ''
                class_level2 = item['subIndustries'][0]['labelName'] if item['subIndustries'] else ''
                csv.loc[csv['ID'] == item['textId'], 'class_level1'] = class_level1
                csv.loc[csv['ID'] == item['textId'], 'class_level2'] = class_level2
        else:
            print('\n', response.json().get('state', ''))

    return csv


def request_keyword(csv):
    url = '/api/nlp/v1/keywords'
    fullurl = get_fullurl('POST', url)
    body = {"items": []}
    num = 0
    while not num == len(csv):
        for i in csv.itertuples():
            num += 1
            if 0 < len(getattr(i, 'text')) < 4096 and num % 20 != 0:
                body['items'].append({
                    "textId": getattr(i, 'ID'),
                    "text": getattr(i, 'text')
                })
        response = requests.post(fullurl, data=json.dumps(body),
                                 headers={"Content-Type": "application/json"},
                                 timeout=(5, 60),
                                 verify=False)
        if response.json().get('state', '') == 'OK':
            for item in response.json().get('body', {}).get('items', []):
                keyword = ''
                item['keywords'].sort(key=lambda x: float(x['weight']), reverse=True)
                for key in item['keywords']:
                    keyword += key['name'] + ' '
                csv.loc[csv['ID'] == item['textId'], 'keywords'] = keyword[:-1]
        else:
            print('\n', response.json())

    print(csv)
    return csv


if __name__ == "__main__":
    # print(json.dumps(parse_news(get_news_list()), indent=2).encode().decode())
    data = request_keyword(request_class(parse_news(get_news_list())))
    num = 0
    for index, rows in data.iterrows():
        raw_content = re.sub(u"([\u000a\u3000\u000d\u0008\u0009])", "", rows["text"])
        keywords = ";".join(rows["keywords"].split(" ")) if rows["keywords"] != "" else ""
        params = {"cate": rows["class_level1"], "title": rows["title"],
                  "content": rows["text"], "keywords": keywords,
                  "length": len(raw_content),
                  "digest": raw_content[:20] if len(raw_content) > 20 else raw_content[:10]}
        with app.app_context():
            news = News(**params)
            db.session.add(news)
            db.session.commit()
            num += 1
    print(num)
