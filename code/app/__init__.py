from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
# from flask_restplus import Api, Resource, fields

from flask_session import Session
from .config import config_map

db = SQLAlchemy()


def create_app(config_name):
    # config_name: 选择环境的参数
    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)  # 从一个类中直接获取配置参数

    # app.secret_key = config_class.SECRET_KEY
    db.init_app(app)  # 实例化数据库

    Session(app)  # 将app中的session数据全部读出来

    @app.route('/')
    def index():
        return send_from_directory("../dist", 'index.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory("../dist", 'favicon.ico')

    """注册蓝图"""
    from . import admin, user, news, cloudAPI
    app.register_blueprint(user.user, url_prefix="/user")
    app.register_blueprint(admin.admin, url_prefix='/admin')
    app.register_blueprint(news.news, url_prefix='/news')
    app.register_blueprint(cloudAPI.cloudAPI, url_prefix='/cloudAPI')

    # """文档配置"""
    # api = Api(app, version='1.0', title='软件杯团队 API', description='A authenticate user and save cloud accounts API')
    # user = api.namespace('user', path='/user')
    # news = api.namespace('cloud accounts', path='/news')
    # cloudAPI = api.namespace('cloudAPI', path='/cloudAPI')
    # admin = api.namespace('admin', path='/admin')
    #
    return app
