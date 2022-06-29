from ..models import News, db, User2News, UserNewsRate, UserNewsClass, User
import math
from sqlalchemy.sql import func


# 分类英文列表
cate_list = ['fiance', 'health_care', 'education', 'tech', 'energy', 'transport',
             'architecture', 'sports', 'military', 'manufacture', 'ecology',
             'travel', 'restaurant', 'agf', 'hot_issue', 'social', 'entertainment',
             'info', 'trans_security', 'social_security', 'disaster']

# 分类中文列表
cate_list_cn = ['金融', '医疗卫生', '教育培训', '科技', '能源矿产', '交通运输', '房产建筑',
                '体育', '军事国防', '制造业', '生态环境', '旅游', '住宿餐饮', '农林牧渔',
                '时政', '社会民生', '文化娱乐', '信息产业', '交通安全', '社会治安',
                '灾害险情'
                '']


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
