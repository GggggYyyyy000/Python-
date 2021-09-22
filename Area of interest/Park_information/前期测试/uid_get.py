import requests
import json
import pandas as pd
import pprint

def geo_address(name,city):
    result = []
    url = "http://api.map.baidu.com/place/v2/search?parameters"
    key = "zfetLGY71RsWuZP3xZKc7WrM0rurWPVd"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"query": name,"region":city, "ak": key, "output": "json"}
    b = requests.get(url, headers=headers, params=keyword, timeout=10)
    if b.status_code == 200:
        html = b.text
        try:
            a = json.loads(html)["results"][0]
            print(a)
            if "uid" in a:
                a.update({"lat": a['location']['lat']})
                a.update({"lng": a['location']['lng']})
                del a['location']
                return a
            else:
                b = {'address': 'none','area': 'none','city': 'none','detail': 'none','lat': 'none','lng': 'none','name': name,'province': 'none','street_id': 'none','telephone': 'none'}
                print("{}值请求失败".format(name))  
                return b  
        except:
            b = {'address': 'none','area': 'none','city': 'none','detail': 'none','lat': 'none','lng': 'none','name': name,'province': 'none','street_id': 'none','telephone': 'none'}
            print("{}值请求失败".format(name))  
            return b 

bf = pd.read_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020 毕业论文/中期检查/厦门数据验证/厦门市公园数据.xlsx")
df = pd.DataFrame(columns=["address","area","city","detail",'lat','lng',"name","province","street_id","telephone","uid"])
for i in range(len(bf)):
    name = bf.loc[i,'公园名称']
    city = bf.loc[i,'城市']
    a = geo_address(name,city)
    a.update({"Last_name": name})
    a.update({"type": bf.loc[i,'公园类型']})
    df = df.append(a,ignore_index=True)

df.to_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020 毕业论文/中期检查/厦门数据验证/厦门市公园数据_uid.xlsx")