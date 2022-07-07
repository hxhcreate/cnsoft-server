from ..models import News, db, User2News, UserNewsRate, UserNewsClass, User
import math
from sqlalchemy.sql import func
from ..config.classfication import *


def news_user_rec(user_id, nums):
    def calc_p(num):
        return math.exp(num - 2) / (math.exp(-1) - math.exp(-2))

    user_news_class = UserNewsClass.query.filter_by(user_id=user_id).first()

    p_list = [calc_p(user_news_class.getItem(cate)) for cate in cate_list]
    print(p_list)
    cate = cate_list[p_list.index(max(p_list))]
    cate = cate_list_cn[cate_list.index(cate)]
    print(cate)
    news = News.query.filter_by(cate=cate).order_by(func.random()).limit(nums).all()

    news_list = [{"newsID": new.id, "cate": cate, "title": new.title,
                  "digest": new.digest, "hpic": new.hpic,
                  "heat": new.heat, "keywords": new.keywords} for new in news]
    return news_list
