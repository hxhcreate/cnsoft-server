import numpy as np
import pandas as pd

from ..models import News, User, db, User2News


def read_news_from_db():
    news_df = pd.DataFrame(columns=['id', 'title', 'cate', 'cate2', 'address', 'heat', 'date', 'source', 'keywords',
                                    'length', 'views', 'loves', 'comments', 'stars'])
    index = 0
    for news_item in News.query.filter_by().all():
        news_dict = news_item.to_dict()
        news_value = [v for k, v in news_dict.items()]
        news_df.loc[index] = news_value
        index += 1
    return news_df

def read_user_rate_news():

