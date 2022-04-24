from . import db
import datetime


class Admin(db.Model):
    __tableName__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)


class User(db.Model):
    __tableName__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    cate = db.Column(db.Enum("pure", "wechat", "phone"))
    nickname = db.Column(db.String(64))
    avatar = db.Column(db.String(64))  # 头像图片的url
    gender = db.Column(db.Enum("male", "female"))
    age = db.Column(db.Integer)
    city = db.Column(db.String(32))
    job = db.Column(db.String(32))
    """其他登录方式"""
    phone = db.Column(db.String(11))
    wechat_id = db.Column(db.String(64))

    """统计信息"""
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now())
    total_read_time = db.Column(db.BigInteger, default=0)  # 单位毫秒
    total_clicks = db.Column(db.BigInteger, default=0)

    """外键关联"""
    user_news = db.relationship("User2News", backref="user")  # 关联到表User2News的
    # user_log = db.relationship("UserLog", backref='user')  # 关联到表UserLog


class News(db.Model):
    __tableName__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(32))
    date = db.Column(db.DATE)
    platform = db.Column(db.String(32))
    keywords = db.Column(db.String(100))
    length = db.Column(db.Integer, default=0)
    total_clicks_by_user = db.Column(db.BigInteger, default=0)
    user_news = db.relationship("User2News", backref='news')  # 关联到表User2News


# really need it?
# class UserLog(db.Model):  # 单次登录的所有浏览记录
#     __tableName__ = 'user_log'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     start_date = db.Column(db.DATE, nullable=False)
#     start_addr = db.Column(db.String(64))
#     stay_time = db.Column(db.Integer, default=0)
#     clicks = db.Column(db.Integer, default=0)


class User2News(db.Model):  # 单次单条浏览记录
    __tableName__ = 'user_news'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DATE, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)
    read_time = db.Column(db.Integer, default=0)
    read_process = db.Column(db.String(5), default="0%")
    is_like = db.Column(db.Boolean)
    is_favorite = db.Column(db.Boolean)


class WeUserToken(db.Model):  # 微信用户登录信息
    __tableName__ = 'we_user_token'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), nullable=False, unique=True)
    code = db.Column(db.String(100), nullable=False, index=True)
    access_token = db.Column(db.String(100), nullable=False, index=True)  # 索引提速
    refresh_token = db.Column(db.String(100), nullable=False, index=True)


class WeUserInfo(db.Model):  # 微信用户个人信息
    __tableName__ = 'we_user_info'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 外键到user_id
    openid = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.Enum("1", "2"), default="")
    province = db.Column(db.String(32), default="")
    city = db.Column(db.String(32), default="")
    country = db.Column(db.String(32), default="")
    head_img_url = db.Column(db.String(100), default="")
    privilege = db.Column(db.String(100), default="")
    union_id = db.Column(db.String(64), default="")
