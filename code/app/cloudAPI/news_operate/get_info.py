import json
import sys
from queue import Queue
from threading import Lock, Thread

lock = Lock()

import requests

requests.packages.urllib3.disable_warnings()

sys.path.append('..')
import multiprocessing
import os

import pandas as pd
from ..Signature import get_fullurl

base_path = '../../../../../THUCNews/'
base_column_field = ['ID', 'class_level0', 'class_level1', 'class_level2', 'title', 'text', 'keywords']


def to_csv_single_class(class_name):
    base_path = '../../../../../THUCNews/'
    base_column_field = ['ID', 'class_level0', 'class_level1', 'class_level2', 'title', 'text', 'keywords']
    ID = 0
    news_table = pd.DataFrame(columns=base_column_field)
    for file_index, file_name in enumerate(os.listdir(base_path + class_name)):
        with open(base_path + class_name + '/' + file_name, encoding='utf-8') as f:
            content = f.read().split('\n', 1)
            if len(content) != 2:
                print("length of news error!")
                continue
            title = content[0]
            text = content[1]
            news_row = pd.Series([ID, class_name, None, None, title, text, None],
                                 index=base_column_field)
            news_row.name = str(ID)
            news_table = pd.concat([news_table, news_row.to_frame().T], ignore_index=True)
            ID += 1
            print(file_index, '/', len(os.listdir(base_path + class_name)), '/', class_name, '\r', end='')
    news_table.to_csv('{}/../news_{}.csv'.format(base_path, class_name))


def to_csv():
    print(os.listdir(base_path))
    pool = multiprocessing.Pool()
    pool.map(to_csv_single_class, os.listdir(base_path))
    pool.close()
    pool.join()


def to_1_csv():
    csv = pd.DataFrame(columns=base_column_field)
    for i in os.listdir(base_path + '../csv/'):
        print(i)
        csv = pd.concat([csv, pd.read_csv(base_path + '../csv/' + i)[:100]], ignore_index=True)
    csv.pop("Unnamed: 0")
    csv["ID"] = csv.index

    csv.to_csv('{}/../news.csv'.format(base_path))


def get_class():
    csv = pd.read_csv(base_path + '../news.csv')
    csv.pop("Unnamed: 0")
    csv[['ID']] = csv[['ID']].astype(str)
    q = Queue()
    step = 20
    threads = []
    for i in range(0, len(csv.index), step):
        t = Thread(target=request_class, args=(
        csv.iloc[i: i + step].copy() if i + step <= len(csv.index) else csv.iloc[i:].copy(), q, len(csv.index) // step,
        step))
        t.start()
        threads.append(t)
        # break
    for t in threads:
        t.join()
    while not q.empty():
        new_csv = q.get()
        for i in new_csv.itertuples():
            csv.loc[csv['ID'] == getattr(i, 'ID'), 'class_level1'] = getattr(i, 'class_level1')
            csv.loc[csv['ID'] == getattr(i, 'ID'), 'class_level2'] = getattr(i, 'class_level2')
    csv.to_csv(base_path + '../news_classified.csv')


def request_class(csv, q: Queue, total_num: int, step: int):
    url = '/api/nlp/v1/industry'
    fullurl = get_fullurl('POST', url)
    body = {"items": []}
    for i in csv.itertuples():
        if len(getattr(i, 'text')) < 4096:
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
        lock.acquire()
        print('\n', response.json().get('state', ''))
        lock.release()

    lock.acquire()
    q.put(csv)
    print('\r', q.qsize(), '/', total_num, end='')
    lock.release()
    pass


def get_keyword():
    csv = pd.read_csv(base_path + '../news_classified.csv')
    csv.pop("Unnamed: 0")
    csv[['ID']] = csv[['ID']].astype(str)
    q = Queue()
    step = 20
    threads = []
    for i in range(0, len(csv.index), step):
        t = Thread(target=request_keyword, args=(
        csv.iloc[i: i + step].copy() if i + step <= len(csv.index) else csv.iloc[i:].copy(), q, len(csv.index) // step,
        step))
        t.start()
        threads.append(t)
        # break
    for t in threads:
        t.join()
    while not q.empty():
        new_csv = q.get()
        for i in new_csv.itertuples():
            csv.loc[csv['ID'] == getattr(i, 'ID'), 'keywords'] = getattr(i, 'keywords')
    csv.to_csv(base_path + '../news_keywords.csv')
    pass


def request_keyword(csv, q: Queue, total_num: int, step: int):
    url = '/api/nlp/v1/keywords'
    fullurl = get_fullurl('POST', url)
    body = {"items": []}
    for i in csv.itertuples():
        if len(getattr(i, 'text')) < 4096:
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
        lock.acquire()
        print('\n', response.json())
        lock.release()

    lock.acquire()
    q.put(csv)
    print('\r', q.qsize(), '/', total_num, end='')
    lock.release()
    pass


def main():
    # to_csv()
    # to_1_csv()
    # get_class()
    get_keyword()
    pass


if __name__ == '__main__':
    main()
