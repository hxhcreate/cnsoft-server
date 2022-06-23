from flask import jsonify
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from . import db
import datetime
import re
from .tools.rsa_tool import rsa_decrypt

default_time_str = "00-01-01 00:00:00"


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)


# 建立三张表的记录
def create_user(username, password):
    user = User(username=username, password=password)
    userlog = UserLog(user_id=user.id)
    User.add(user)
    UserLog.add(userlog)


class Admin(db.Model):
    __tableName__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    @staticmethod
    def select_by_id(id):
        return Admin.query.filter_by(id=id).first()


class User(db.Model):
    __tableName__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    nickname = db.Column(db.String(64), default="")
    avatar = db.Column(db.String(200), default='')  # 头像图片的url
    gender = db.Column(db.Enum("male", "female"), default='')
    age = db.Column(db.Integer, default=0)
    country = db.Column(db.String(64), default='')
    province = db.Column(db.String(64), default='')
    city = db.Column(db.String(64), default='')
    job = db.Column(db.String(64), default='')
    """其他登录方式"""
    phone = db.Column(db.String(11), default='')
    wechat_id = db.Column(db.String(64), default='', unique=True)  # 对应微信unionid

    """统计信息"""
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 不加括号表示不更新时间
    total_read_time = db.Column(db.BigInteger, default=0)  # 单位毫秒
    total_clicks = db.Column(db.BigInteger, default=0)

    """外键关联"""
    user_news = db.relationship("User2News", backref="user")  # 关联到表User2News的

    # user_log = db.relationship("UserLog", backref='user')  # 关联到表UserLog

    @orm.reconstructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.k = v

    def __dic__(self):
        pass

    @staticmethod
    def add(user):
        db.session.add(user)
        session_commit()

    @staticmethod
    def delete(id):
        User.query.filter_by(id=id).delete()
        return session_commit()

    def update_user_info(self, **kwargs):
        for k, v in kwargs.items():
            self.k = v
        db.session.add(self)
        session_commit()

    @staticmethod
    def update():
        session_commit()

    @staticmethod
    def select_user_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def select_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def is_exist_user_by_username(username):
        old_users = User.query.filter_by(username=username).all()
        if len(old_users) > 0:
            return True
        return False

    @staticmethod
    def check_password(password, crypto):
        if password == rsa_decrypt(crypto):
            return True
        return False

    @staticmethod
    def decode_password(crypto):
        return rsa_decrypt(crypto)


class News(db.Model):
    __tableName__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), default="")
    digest = db.Column(db.Text, default="")
    cate = db.Column(db.String(16), nullable=False)
    cate2 = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(64), default="")
    hpic = db.Column(db.String(255), default="")  # 头部图片Url
    heat = db.Column(db.Float, default=0)  # 新闻热度 浮点型
    date = db.Column(db.DateTime, default=datetime.datetime.strptime(default_time_str, "%y-%m-%d %H:%M:%S"))
    source = db.Column(db.String(32), default="")
    keywords = db.Column(db.String(255), default="")  # join by ;
    length = db.Column(db.Integer, default=0)  # 创建该对象不会默认  上传之后在数据库层面会默认为0
    content = db.Column(db.Text(16777216), default="")
    views = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    stars = db.Column(db.Integer, default=0)
    user_news = db.relationship("User2News", backref='news')  # 关联到表User2News

    @orm.reconstructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.k = v

    def to_dict(self):
        # 用来推荐的，不要改
        news_dict = {
            "id": self.id,
            "title": self.title,
            "cate": self.cate,
            "cate2": self.cate2,
            "address": self.address,
            "heat": self.heat,
            "date": self.date,
            "source": self.source,
            "keywords": self.keywords,
            "length": self.length,
            "views": self.views,
            "loves": self.loves,
            "comments": self.comments,
            "stars": self.stars
        }
        return news_dict

    @staticmethod
    def add(news):
        db.session.add(news)
        session_commit()

    @staticmethod
    def select_news_by_id(id):
        news = News.query.filter_by(id=id).first()
        if isinstance(news, [None]):
            raise Exception

    def __getitem__(self, item):
        return self.item

    def increase_love(self):
        self.loves += 1

    def increase_view(self):
        self.views += 1

    def increase_star(self):
        self.stars += 1

    def increase_comment(self):
        self.comments += 1


# 暂时用于推荐算法
class UserNewsClass(db.Model):
    __tableName__ = 'user_news_class'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fiance = db.Column(db.Integer, default=0)
    health_care = db.Column(db.Integer, default=0)
    education = db.Column(db.Integer, default=0)
    tech = db.Column(db.Integer, default=0)
    energy = db.Column(db.Integer, default=0)
    transport = db.Column(db.Integer, default=0)
    architecture = db.Column(db.Integer, default=0)
    sports = db.Column(db.Integer, default=0)
    military = db.Column(db.Integer, default=0)
    manufacture = db.Column(db.Integer, default=0)
    ecology = db.Column(db.Integer, default=0)
    travel = db.Column(db.Integer, default=0)
    restaurant = db.Column(db.Integer, default=0)
    agf = db.Column(db.Integer, default=0)
    hot_issue = db.Column(db.Integer, default=0)
    social = db.Column(db.Integer, default=0)
    entertainment = db.Column(db.Integer, default=0)
    info = db.Column(db.Integer, default=0)
    trans_security = db.Column(db.Integer, default=0)
    social_security = db.Column(db.Integer, default=0)
    disaster = db.Column(db.Integer, default=0)

    def getItem(self, name):
        self.name


# 用户浏览汇总
class UserLog(db.Model):  # 单次登录的所有浏览记录
    __tableName__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    rec_news_list = db.Column(db.Text(16777216), default='')  # 曾经推送过哪些新闻，;分割的id
    liked_news_list = db.Column(db.Text(16777216), default='')
    stared_news_list = db.Column(db.Text(16777216), default='')

    @staticmethod
    def add(user_log):
        db.session.add(user_log)
        session_commit()

    @staticmethod
    def parse_news_list(ori_string):
        string = ori_string
        return map(lambda item: eval(item), string.split(";"))

    def add_rec_news_list(self, list):
        list_str = ";".join(map(lambda item: str(item), list))
        self.rec_news_list = self.rec_news_list + ";" + list_str
        db.session.add(self)
        session_commit()

    def add_liked_news_list(self, list):
        list_str = ";".join(map(lambda item: str(item), list))
        self.liked_news_list = self.liked_news_list + ";" + list_str
        db.session.add(self)
        session_commit()

    def add_stared_news_list(self, list):
        list_str = ";".join(map(lambda item: str(item), list))
        self.stared_news_list = self.stared_news_list + ";" + list_str
        db.session.add(self)
        session_commit()


# 暂时不使用评分表
class UserNewsRate(db.Model):  # 用户评分总记录
    __tableName__ = 'user_news_rate'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    news_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, default=0)
    is_like = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)

    def rating(self):
        if User2News.is_liked(self.user_id, self.news_id):
            self.is_like = True
        if User2News.is_favorite(self.user_id, self.news_id):
            self.is_favorite = True
        if self.is_like and self.is_favorite:  # 浏览且duoble
            self.rate = 3
        elif self.is_like or self.is_favorite:  # 浏览且点赞或者浏览且收藏
            self.rate = 2
        else:  # 推荐但未
            # 浏览
            self.rate = 1


class User2News(db.Model):  # 单次单条浏览记录
    __tableName__ = 'user_news'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)
    read_time = db.Column(db.Integer, default=0)
    read_process = db.Column(db.String(5), default="0%")
    is_like = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)

    @staticmethod
    def is_liked(user_id, news_id):
        for item in User2News.query.filter_by(user_id=user_id, news_id=news_id).all():
            if item is not None and item.is_like:
                return True
        return False

    @staticmethod
    def is_favorite(user_id, news_id):
        for item in User2News.query.filter_by(user_id=user_id, news_id=news_id).all():
            if item is not None and item.is_favorite:
                return True
        return False


class WeUserToken(db.Model):  # 微信用户登录信息
    __tableName__ = 'we_user_token'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(255), nullable=False, index=True)
    access_token = db.Column(db.String(255), nullable=False, index=True)  # 索引提速
    refresh_token = db.Column(db.String(255), nullable=False, index=True)
    unionid = db.Column(db.String(255), index=True, nullable=False, unique=True)


class WeUserInfo(db.Model):  # 微信用户个人信息
    __tableName__ = 'we_user_info'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.Integer, default=1)
    province = db.Column(db.String(32), default="")
    city = db.Column(db.String(32), default="")
    country = db.Column(db.String(32), default="")
    headimgurl = db.Column(db.String(512), default="")
    privilege = db.Column(db.String(512), default="")
    unionid = db.Column(db.String(255), nullable=False, unique=True)

    @orm.reconstructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.k = v
