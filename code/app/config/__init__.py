SERVER_PORT = 5001

# MD5设置
MD5_SALT = "2022soft"

# wechat配置
app_id = None
secret = None

# redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
WECHAT_ACCESS_EXPIRE_TIME = 10000000
SESSION_EXPIRE_TIME = 1000
DEV_DB = 1
PRO_DB = 2

# import redis
# redis_store = redis.Redis(host='127.0.0.1', port=6379)  # 操作的redis配置


# 基础环境
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"
    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理 加密混淆
    PERMANENT_SESSION_LIFETIME = SESSION_EXPIRE_TIME  # session数据的有效期，单位秒


# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/2022soft'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379)
    DEBUG = True


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/2022soft'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379)


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
