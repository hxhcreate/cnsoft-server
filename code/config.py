SERVER_PORT = 5000

import redis

redis_store = redis.Redis(host='127.0.0.1', port=6379, db=1)  # 操作的redis配置


# 基础环境
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"
    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理 加密混淆
    PERMANENT_SESSION_LIFETIME = 100  # session数据的有效期，单位秒


# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/2022soft'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=1)
    DEBUG = True


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/2022soft'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=1)


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
