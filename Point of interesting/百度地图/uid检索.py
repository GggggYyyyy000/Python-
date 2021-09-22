import pandas as pd
import requests
from transCoordinateSystem import bd09_to_wgs84

import pprint

def uid_get(file_path):
    a = pd.read_excel(file_path)
    uid = []
    for i in range(len(a)):
        uid.append(a.loc[i,"uid"])
    return uid

def baidu_api(uid):
    import json
    url = "http://api.map.baidu.com/place/v2/detail?"
    key = "zfetLGY71RsWuZP3xZKc7WrM0rurWPVd"
    keywords = {"ak": key, "uid": uid, "scope": "2", "output": "json"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    a = requests.get(url, params=keywords, headers=headers)
    if a.status_code == 200:
        html = a.text   
        json = json.loads(html)
        try:
            rate = json["result"]["detail_info"]["overall_rating"]
        except:
            rate = 0
        lat = json["result"]["location"]["lat"]
        lng = json["result"]["location"]["lng"]
        coord_wgs84 = bd09_to_wgs84(float(lng), float(lat))
        lng = coord_wgs84[0]
        lat = coord_wgs84[1]
        infor = {"name":json["result"]["name"],
                "city":json["result"]["city"],
                "area":json["result"]["area"],
                "address":json["result"]["address"],
                "rate":rate,
                "lat":lat,
                "lng":lng,
                "uid":json["result"]["uid"]}
        print (infor)
    return infor
        
file_path = "D:\\2020 毕业论文\\数据收集\\公园\\案例公园选择.xlsx"
df = pd.DataFrame(columns=["name","city","area","address","rate","lat","lng","uid"])
data = []
uid = uid_get(file_path)

for i in uid:
    infor = baidu_api(i)
    data.append(infor)

df = df.append(data,ignore_index=True)
df.to_excel("information_uid.xlsx")





