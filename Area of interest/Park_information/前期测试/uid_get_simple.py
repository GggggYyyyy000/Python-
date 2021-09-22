import requests
import json
import pandas as pd
import pprint

def geo_address(uid):
    url = "http://api.map.baidu.com/place/v2/detail?parameters"
    key = "zfetLGY71RsWuZP3xZKc7WrM0rurWPVd"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"uid": uid,"scope":"2", "ak": key, "output": "json"}
    b = requests.get(url, headers=headers, params=keyword, timeout=10)
    if b.status_code == 200:
        html = b.text
        try:
            a = json.loads(html)["result"]
            a.update({"tag": a['detail_info']['tag']})
            a.update({"lat": a['location']['lat']})
            a.update({"lng": a['location']['lng']})
            del a['location']
            del a['detail_info']
            return a
        except:
            b = {'address': 'none','area': 'none','city': 'none','detail': 'none','lat': 'none','lng': 'none','name': "none",'province': 'none','street_id': 'none','tag': 'none','uid': uid}
            print("{}值请求失败".format(uid))  
            return b


bf = pd.read_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020 毕业论文/中期检查/厦门数据验证/厦门市公园数据_uid.xlsx")
df = pd.DataFrame(columns=["address","area","city","detail",'lat','lng',"name","province","street_id","tag","uid"])
for i in range(len(bf)):
    uid = bf.loc[i,"uid"]
    if uid == "1":
        pass
    else:
        a = geo_address(uid)
        pprint.pprint(a)
        a.update({"Last_name":  bf.loc[i,'Last_name']})
        a.update({"type": bf.loc[i,'type']})
        df = df.append(a,ignore_index=True)

df.to_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020 毕业论文/中期检查/厦门数据验证/厦门市公园数据_uid_uid.xlsx")




            



