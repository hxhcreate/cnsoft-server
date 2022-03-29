# -*- coding = utf-8 -*-
# @Time : 2022/3/29 21:02
# @Author : AuYang
# @File : app.py
# @Software : PyCharm

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"