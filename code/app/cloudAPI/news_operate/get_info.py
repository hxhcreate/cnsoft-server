import requests
import json
import sys
sys.path.append('..')
import os
# from Signature import get_fullurl
import multiprocessing

import pandas as pd

base_path = '../../../../../THUCNews/'

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
    # ID = 0
    # news_table = pd.DataFrame(columns=base_column_field)
    # for class_index, class_name in enumerate(os.listdir()):
    #     for file_index, file_name in enumerate(os.listdir(class_name)):
    #         with open(class_name + '/' + file_name, encoding='utf-8') as f:
    #             content = f.read().split('\n', 1)
    #             if len(content) != 2:
    #                 print("length of news error!")
    #                 continue
    #             title = content[0]
    #             text = content[1]
    #             news_row = pd.Series([ID, class_name, None, None, title, text, None], 
    #                         index=base_column_field)
    #             news_row.name = str(ID)
    #             news_table = pd.concat([news_table, news_row.to_frame().T], ignore_index=True)
    #             ID += 1
    #             print(file_index, '/', len(os.listdir(class_name)), '/', class_name, '\r', end='')
    # news_table.to_csv('../news.csv')
    # print(news_table)

def main():
    to_csv()

if __name__ == '__main__':
    main()
