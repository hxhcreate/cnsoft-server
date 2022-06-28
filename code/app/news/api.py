import datetime
import math
from flask import request, jsonify, session

from . import news
from ..models import News, db, User2News, UserNewsRate, UserNewsClass, User
from sqlalchemy.sql import func
from ..tools.token import Token
from .func import news_user_rec


@news.route("/add", methods=['POST'])
def news_add():  # 需要客户端的请求字段跟Model匹配不然会出错
    json = request.get_json()
    # title = json.get("title", "").strip()
    # digest = json.get("digest", "").strip()
    # cate = json.get("cate", "").strip()
    # address = json.get("address", "").strip()
    # date = json.get("date", "").strip()
    # source = json.get("source", "").strip()
    # keywords = json.get("keywords", "").strip()
    # content = json.get("content", "").strip()
    # length = json.get("length", "").strip()
    try:
        news = News(**json)
        News.add(news)
        return jsonify(msg='增加新闻成功', code=200)
    except Exception as e:
        print(e)
        return jsonify(msg='增加新闻失败', code=402)


@news.route("/feed", methods=['GET'])  # 获取用户新闻列表
def news_feed():
    try:
        userID = int(request.args.get("userID", '').strip())
        token = request.cookies.get("cookies", "").strip()
        cate = request.args.get("cate", "").strip()
        num = request.args.get("num", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        token_value = Token.get_token_value(token)
        token_user_id = token_value[0]
        # 鉴别失败或者获取到category  则认为随机选取
        if userID != int(token_user_id) or cate != "":
            print("token not match userid, no user recommendation!")
            news_list = News.query.filter_by(cate2=cate).sort_by(News.heat).limit(num).all()
            return jsonify(msg="no user rec, success!", code=200, data={'news-list': news_list})
        if cate == "" and userID == int(token_user_id):
            news_list = news_user_rec(userID, num)
            return jsonify(msg="user rec, success!", code=200, data={'news-list': news_list})
    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


@news.route("/content", methods=['GET'])
def get_news_content():
    try:
        newsID = int(request.args.get("newsID", '').strip())
        token = request.cookies.get("cookies", "").strip()
        if not token:
            return jsonify(msg="token is needed", code=4000)
        if not Token.token_is_valid(token):
            return jsonify(msg="token invalid", code=4000)
        data = {}


    except Exception as e:
        print(e)
        return jsonify(msg='kernel error', code=4000)


# 基本刷新推荐
@news.route("/rec/circle", methods=['GET'])
def news_rec_circle():
    cate_list = ['fiance', 'health_care', 'education', 'tech', 'energy', 'transport',
                 'architecture', 'sports', 'military', ' manufacture', 'ecology',
                 'travel', 'restaurant', 'agf', 'hot_issue', 'social', 'entertainment',
                 'info', 'trans_security', 'social_security', 'disaster']

    def calc_p(num):
        return math.exp(num - 2) / (math.exp(-1) - math.exp(-2))

    user_id = request.args.get("userID", "").strip()
    nums = request.args.get("userID", "").strip()
    user_news_class = UserNewsClass.query.filter_by(user_id=user_id).first()
    p_list = [calc_p(user_news_class.getItem(cate)) for cate in cate_list]
    cate = cate_list[cate_list.index(max(p_list))]
    news = News.query.filter_by(cate2=cate).order_by(func.random()).limit(nums).all()
    news_list = [{"newsID": new.id, "cate": cate, "title": new.title,
                  "digest": new.digest, "Hpic": new.hpic,
                  "heat": new.heat, "tag": new.keywords} for new in news]
    return jsonify(msg='获取刷新推荐新闻列表成功', code=200, data={"nums": nums, "news_list": news_list})


@news.route("/rec/window", methods=['GET'])
def news_rec_window():
    pass


@news.route("/rec/hot", methods=['GET'])
def news_rec_hot():
    pass


@news.route("/onClick", methods=['GET'])
def news_click():
    news_id = request.args.get("newsID", "").strip()
    user_id = request.args.get("userID", "").strip()
    sign = request.args.get("sign", "").strip()
    if news_id and user_id and sign:
        try:
            news = News.query.filter_by(id=news_id).first()
            news.increase_view()
            #     创建用户日志  和  用户评分表  和 用户新闻分类个数表
            user_log = User2News(start_time=datetime.datetime.now(), user_id=user_id, news_id=news_id)
            user_news_rate = UserNewsRate(user_id=user_id, news_id=news_id)
            user_news_class = UserNewsClass(user_id=user_id)
            user_news_class.getItem += 1
            db.session.add(user_news_class)
            db.session.add(news)
            db.session.add(user_log)
            db.session.add(user_news_rate)
            db.session.commit()
            return jsonify(msg='success', code=200, data={"logID": user_log.id,
                                                          "userID": user_id,
                                                          "newsID": news_id})
        except Exception as e:
            print(e)
            return jsonify(msg='error', code=403)
    return jsonify(msg='error', code=403)


@news.route("/onLove", methods=['GET'])
def news_love():
    news_id = request.args.get("newsID", "").strip()
    user_id = request.args.get("userID", "").strip()
    sign = request.args.get("sign", "").strip()
    if news_id and user_id and sign:
        try:
            news = News.query.filter_by(id=news_id).first()
            news.increase_love()
            db.session.add(news)
            db.session.commit()
            return jsonify(msg='success', code=200, data={"num": news.loves})
        except Exception as e:
            print(e)
            return jsonify(msg='error', code=403)
    return jsonify(msg='error', code=403)


@news.route("/onStar", methods=['GET'])
def news_star():
    news_id = request.args.get("newsID", "").strip()
    user_id = request.args.get("userID", "").strip()
    sign = request.args.get("sign", "").strip()
    if news_id and user_id and sign:
        try:
            news = News.query.filter_by(id=news_id).first()
            news.increase_star()
            db.session.add(news)
            db.session.commit()
            return jsonify(msg='success', code=200, data={"num": news.stars})
        except Exception as e:
            print(e)
            return jsonify(msg='error', code=403)
    return jsonify(msg='error', code=403)
