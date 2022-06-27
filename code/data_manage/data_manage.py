import pandas as pd
import re
# 将上一级的目录加入到import目录中
import sys

sys.path.append('..')
from app import db  # 引入的是manage中已经实例化app的db
from app import create_app
from app.models import News

app = create_app("product")  


def insertManyNews(file_path):
    data = pd.read_csv(file_path, encoding="utf-8")
    data = data.fillna("")
    num = 0
    for index, rows in data.iterrows():
        raw_content = re.sub(u"([\u000a\u3000\u000d\u0008\u0009])", "", rows["text"])
        keywords = ";".join(rows["keywords"].split(" ")) if rows["keywords"] != "" else ""
        params = {"cate": rows["class_level0"], "cate2": rows["class_level1"], "title": rows["title"],
                  "content": rows["text"], "keywords": keywords,
                  "length": len(raw_content),
                  "digest": raw_content[:20] if len(raw_content) > 20 else raw_content[:10]}
        with app.app_context():
            news = News(**params)
            db.session.add(news)
            db.session.commit()
            num += 1
    print(num)


if __name__ == '__main__':
    insertManyNews("news.csv")
