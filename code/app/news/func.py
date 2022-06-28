from ..models import News, db, User2News, UserNewsRate, UserNewsClass, User
import math
from sqlalchemy.sql import func


def news_user_rec(user_id, nums):
    cate_list = ['fiance', 'health_care', 'education', 'tech', 'energy', 'transport',
                 'architecture', 'sports', 'military', ' manufacture', 'ecology',
                 'travel', 'restaurant', 'agf', 'hot_issue', 'social', 'entertainment',
                 'info', 'trans_security', 'social_security', 'disaster']

    def calc_p(num):
        return math.exp(num - 2) / (math.exp(-1) - math.exp(-2))

    user_news_class = UserNewsClass.query.filter_by(user_id=user_id).first()
    p_list = [calc_p(user_news_class.getItem(cate)) for cate in cate_list]
    cate = cate_list[cate_list.index(max(p_list))]
    news = News.query.filter_by(cate2=cate).order_by(func.random()).limit(nums).all()
    news_list = [{"newsID": new.id, "cate": cate, "title": new.title,
                  "digest": new.digest, "hpic": new.hpic,
                  "heat": new.heat, "keywords": new.keywords} for new in news]
    return news_list
