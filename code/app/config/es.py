from elasticsearch import Elasticsearch

from ..models import db, News


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
                    "address": {
                        "type": "text"
                    },
                    "hpic": {
                        "type": "text"
                    },
                    "heat": {
                        'type': "double"
                    },
                    "date": {
                        "type": "date"
                    },
                    "source": {
                        "type": "text"
                    },
                    "keywords": {
                        "type": "text"
                    },
                    "length": {
                        "type": "integer"
                    },
                    "content": {
                        "type": "text"
                    },
                    "views": {
                        "type": "integer"
                    },
                    "loves": {
                        "type": "integer"
                    },
                    "comments": {
                        "type": "integer"
                    },
                    "stars": {
                        "type": "integer"
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

    def search(self, search_input, nums=10):
        body = {
            "query": {
                "bool": {
                    "should": [
                        # {
                        #     "match": {
                        #         "keywords": search_input
                        #     }
                        # },
                        {
                            "match": {
                                "title": search_input
                            }
                        },
                        {
                            "term": {
                                "cate": search_input
                            }
                        },
                        {
                            "term": {
                                "cate2": search_input
                            }
                        }
                    ]
                }
            },
            "_source": ["id", 'title', 'date', 'heat', 'hpic'],
            "from": 0,
            "size": nums,
            "highlight": {
                "boundary_scanner": "sentence",
                "pre_tags": "<em>",
                "post_tags": "</em>",
                "fields": {
                    "title": {
                        "pre_tags": [
                            "<h1>"
                        ],
                        "post_tags": [
                            "</h1>"
                        ]
                    }
                }
            }
        }
        re = self.es.search(index=self.index, body=body)
        print(re)
        id_list = [item['_source']['id'] for item in re['hits']['hits']]
        print(id_list)
        return id_list


es = ESClient(hosts=[{'host': "127.0.0.1", "port": 9200}], index="2022soft_news")
