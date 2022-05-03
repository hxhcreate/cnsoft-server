import time
import pandas as pd
import requests
import json
import re


def test():
    data = pd.read_csv("../app/tools/news.csv", encoding="utf-8")
    data = data.fillna("")
    num = 0
    for index, news in data.iterrows():
        print(news['class_level1'])
        if news["class_level1"] != "":
            num += 1
    print(num)


def main():
    data = pd.read_csv("../app/tools/news.csv", encoding="utf-8")
    data = data.fillna("")
    num = 0
    for index, news in data.iterrows():
        raw_content = re.sub(u"([\u000a\u3000\u000d\u0008\u0009])", "", news["text"])
        keywords = ";".join(news["keywords"].split(" ")) if news["keywords"] != "" else ""
        params = {"cate": news["class_level0"], "cate2": news["class_level1"], "title": news["title"],
                  "content": news["text"], "keywords": keywords,
                  "length": len(raw_content),
                  "digest": raw_content[:20] if len(raw_content) > 20 else raw_content[:10]}
        print(params)
        r = requests.post("http://127.0.0.1:5001/news/add", json=params)
        if json.loads(r.text)["code"] != 200:
            break
        num += 1
        time.sleep(0.05)
    print(num)


if __name__ == "__main__":
    main()
