from elasticsearch import Elasticsearch
import datetime
import json
from functools import wraps

import sys

sys.path.append('..')
from app import db  # 引入的是manage中已经实例化app的db
from app import create_app
from app.models import News

app = create_app("develop")

class ESClient:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.index = kwargs['index']
        self.mapping = self.get_mapping()
        self.es = Elasticsearch(hosts=self.hosts,
                                sniff_on_start=True,  # 连接前测试
                                sniff_timeout=60,
                                sniff_on_connection_fail=True)  # 刷新节点
        self.build_index()

    # 从sql中获取数据
    def get_data_from_mysql(self):
        with app.app_context():
            news_list = News.query.all()
            for news in news_list:
                params = {
                    "id": news.id,
                    "title": news.title,
                    "digest": news.digest,
                    "cate": news.cate,
                    "cate2": news.cate2,
                    "date": news.date,
                    "address": news.address,
                    "source": news.source,
                    "hpic": news.hpic,
                    "heat": news.heat,
                    "keywords": news.keywords
                }
                self.add_doc(params)

    def get_mapping(self):
        return {
            "mappings": {
                'properties': {
                    "id": {
                        "type": "integer"
                    },
                    'title': {
                        'type': "text"
                    },
                    "digest": {
                        'type': "text"
                    },
                    "cate": {
                        'type': "keyword"
                    },
                    "cate2": {
                        'type': "keyword"
                    },
                    "date": {
                        "type": "date"
                    },
                    "address": {
                        "type": "text"
                    },
                    "source": {
                        "type": "text"
                    },
                    "hpic": {
                        "type": "text"
                    },
                    "heat": {
                        'type': "double"
                    },
                    "keywords": {
                        "type": "text"
                    }
                }
            }
        }

    def delete_index(self):
        return self.es.indices.delete(index=self.index)

    def build_index(self, overwrite=False):
        if self.es.indices.exists(self.index):
            if overwrite:
                self.delete_index()
                print("index {} has been deleted.".format(self.index))
            else:
                print("The index {} already exists, "
                      "if you want to delete it, set overwrite to True")
                return
        self.es.indices.create(index=self.index, body=self.mapping)
        print("Index {} has been built.".format(self.index))

    def put_mapping(self, body):
        self.es.indices.put_mapping(index=self.index, body=body)

    def add_doc(self, doc):
        self.es.index(index=self.index, body=doc)

    # @index_exists()
    # def search(self, search_input):
    #     body = {
    #         "query": {
    #             "bool": {
    #                 "should": [
    #                     "match": {},
    #                 ]
    #             }
    #         }
    #     }


if __name__ == "__main__":
    es = ESClient(hosts=[{'host': "127.0.0.1", "port": 9200}], index="2022soft")
    # es.get_data_from_mysql()
