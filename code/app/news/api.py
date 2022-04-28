import datetime

from flask import request, jsonify, session

from . import news
from ..models import News, db, User2News


@news.route("/feed", methods=['GET'])  # 获取用户新闻列表
def news_feed():
    cate = request.args.get("cate", "").strip()
    sign = request.args.get("sign", "").strip()
    nums = request.args.get('nums', "0").strip()
    if cate != "" and nums != '0':
        try:
            news = News.query.filter_by(cate=cate).order_by(News.heat.desc()).limit(nums).all()
            news_list = [{"newsID": new.id, "cate": cate, "title": new.title,
                          "digest": new.digest, "Hpic": new.hpic,
                          "heat": new.heat, "tag": new.keywords} for new in news]
            return jsonify(msg='获取新闻列表成功', code=200, nums=nums, news_list=news_list)
        except Exception as e:
            print(e)
            return jsonify(msg='error', code=403)
    return jsonify(msg='error', code=403)


@news.route("/getNewsContent", methods=['GET'])
def get_news_content():
    news_id = request.args.get("newsID", "").strip()
    sign = request.args.get("sign", "").strip()
    if news_id and sign:
        try:
            news = News.query.filter_by(id=news_id).first()
            return jsonify(msg='success', code=200, data={
                'newsID': news.id, 'cate': news.cate,
                'title': news.title, "heat": news.heat,
                'time': news.date.strftime("%Y-%m-%d %H:%M:%S"), "source": news.source,
                'content': news.content, 'viewNum': news.views, 'loveNum': news.loves,
                'commentNum': news.comments, 'starNum': news.stars
            })
        except Exception as e:
            print(e)
            return jsonify(msg='error', code=403)
    return jsonify(msg='error', code=403)


@news.route("/onClick", methods=['GET'])
def news_click():
    news_id = request.args.get("newsID", "").strip()
    user_id = request.args.get("userID", "").strip()
    sign = request.args.get("sign", "").strip()
    if news_id and user_id and sign:
        try:
            news = News.query.filter_by(id=news_id).first()
            news.increase_view()
            #     创建日志记录
            user_log = User2News(start_time=datetime.datetime.now(), user_id=user_id, news_id=news_id)
            db.session.add(news)
            db.session.add(user_log)
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
