from app import db


class User(db.Model):
    __tableName__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.Enum("male", "female"))
    age = db.Column(db.Integer)
    address = db.Column(db.String(64))
    job = db.Column(db.String(32))
    totalReadTime = db.Column(db.BigInteger, default=0)  # 单位毫秒
    totalClicks = db.Column(db.BigInteger, default=0)
    user2News = db.relationship("User2News", backref="user")  # 关联到表4的
    userLog = db.relationship("UserLog", backref='user')  # 关联到表3


class News(db.Model):
    __tableName__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(32))
    date = db.Column(db.DATE)
    platform = db.Column(db.String(32))
    keywords = db.Column(db.String(100))
    length = db.Column(db.Integer, default=0)
    totalClicksByUser = db.Column(db.BigInteger, default=0)
    user2News = db.relationship("User2News", backref='news')  # 关联到表4


class UserLog(db.Model):
    __tableName__ = 'userLog'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    startDate = db.Column(db.DATE, nullable=False)
    startAddr = db.Column(db.String(64))
    stayTime = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)


class User2News(db.Model):
    __tableName__ = 'user2News'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    newsID = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)
    readTime = db.Column(db.Integer, default=0)
    readProcess = db.Column(db.String(5), default="0%")
    isLike = db.Column(db.Boolean)
    isFavorite = db.Column(db.Boolean)
