import hashlib
import base64
import hmac
import requests
import json
import feedparser
import time

def rss(text):
    database = {"城市规划学刊":'https://navi.cnki.net/knavi/rss/CXGH',
                    "城市规划":"https://nxgp.cnki.net/knavi/rss/CSGH",
                    "地理科学":"https://nxgp.cnki.net/knavi/rss/DLKX",
                    "cities":"http://rss.sciencedirect.com/publication/science/02642751"}
    d = feedparser.parse(database[text])
    datas = []
    for i in d["entries"]:
        data = {"title":i["title"],"author":i["author"],"time":i["published"],
        "abstract":i["summary"],"link":i["link"]}
        x = "[**"  + data["title"] + "**](" + data["link"] + ")\n**" + data["author"] + "**\n"+ data["abstract"]
        datas.append(x)          
    xx = '\n\n'.join(datas)

    url='https://open.feishu.cn/open-apis/bot/v2/hook/12e9feba-4c52-4393-ba59-153ebc8a03e9'
    program={
    "msg_type": "interactive",
    "card":{"card_link": {"url": "https://open.feishu.cn"},
    "config": {
        "wide_screen_mode": True},
        "elements": [{"tag": "div","text": {"content": xx,"tag": "lark_md"}},],
        "header": {"template": "red","title": 
        {"content": "🎉 #" + text +" 8月最新文章# 看看这个月都有哪些文献值得阅读？",
        "tag": "plain_text"}}}}

    headers={'Content-Type': 'application/json'}
    f=requests.post(url,data=json.dumps(program),headers=headers)

text = ["cities"]

for i in text:
    print(i)
    rss(i)