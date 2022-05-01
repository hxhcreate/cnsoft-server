from elasticsearch import Elasticsearch
import datetime
import json


class ESClient:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.port = kwargs['port']
        self.index = kwargs['index']
        self.mapping = self.get_mapping()
        self.es = Elasticsearch(hosts=self.hosts,
                                port=self.port,
                                sniff_on_start=True,  # 连接前测试
                                sniff_timeout=60,
                                sniff_on_connection_fail=True)  # 刷新节点

    def get_mapping(self):
        raise NotImplemented

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
        self.es.indices.create(index=self.index, body=self.mapping)
        print("Index {} has been built.".format(self.index))

    def put_mapping(self, body):
        self.es.indices.put_mapping(index=self.index, body=body)



