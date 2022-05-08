SERVER_PORT = 5001

# MD5设置
MD5_SALT = "2022soft"

# pscs#1格式公钥 私钥配置
PRIVATE_KEY = "MIICXAIBAAKBgQCBavyp/nXGyAdoRlyiIipKm7bvX2utsYDM9yss3bv5brtUiuqcfTyT+lzJwY8" \
              "lOO8FBAGQSUJsZr0xt514Z1hILzN3mBUUlQRrWiacuB1vA8SOVqh9frtyOBUsaQV6f21kD0Dec+BL3r" \
              "s4VODtkCApy2//02/Maq3QHvP+5JTbTwIDAQABAoGAAVu4mXt7YUyMe1qFsrPuGAizWPwk5VagFfFK1DaN" \
              "jawiWNxOYw8TbtrT/3rBwFptHnMw0FgHKPEZGjz68PO7YvPv3hI0V7z5e9R8byzpygpJh0Rh89Mb/AVTbWqKz" \
              "svhR36Nb/E6ylT4+vy67h/fOYVYYRD+nPsa/29j5cHpD5kCQQCLSjTUKwcDb0dZr73bsjb26HTowjlScfsn6F4IY" \
              "I3mSNdU+qWXyTaTvA5q5q8qcsRrAbrJt2K+CuJM2UYmCjy3AkEA7ds9J+ClTSRxHfRcOCzVZKtimK5MtdFTV5domM" \
              "KyZ9zD35SBrvgrRyiddeMZMMJm9qTT0TSrSIbwKFO8GnnuKQJAfzUKAio5gX2DH/lL3vRnFh89hcS7LPxDbzLbjbMAZKtp" \
              "XIZ77J8qZMl+MUrz9kRR9Zfiyo3cc8rk2WIkmmEHCQJBALKlswYrhRwuncM40LbkfZYx30j7yOPah7VHJClwOl0mA/v+Z3TKMn8ssy9i1X241Wq0" \
              "m98Kpwc/SkuPsL1WDRkCQBTcbyMtCBg/3furf1P637g3fFn/CCOBkL2Fd9dqtKdagAyE/oeF4HcL6uzjybin6TDMus+QKnVdsNHnQYmG2iU="

PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCBavyp/nXGyAd" \
             "oRlyiIipKm7bvX2utsYDM9yss3bv5brtUiuqcfTyT+lzJwY8lOO8FBAGQ" \
             "SUJsZr0xt514Z1hILzN3mBUUlQRrWiacuB1vA8SOVqh9frtyOBUsaQV6f21kD0D" \
             "ec+BL3rs4VODtkCApy2//02/Maq3QHvP+5JTbTwIDAQAB"

SECRET_KEY = "easy reading"

# wechat配置
app_id = None
secret = None

# redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
WECHAT_ACCESS_EXPIRE_TIME = 10000000
SESSION_EXPIRE_TIME = 10000
DEV_DB = 1
PRO_DB = 2

import redis


# redis_store = redis.Redis(host='127.0.0.1', port=6379)  # 操作的redis配置
#

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
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=DEV_DB)
    DEBUG = True


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/2022soft'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=PRO_DB)


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
