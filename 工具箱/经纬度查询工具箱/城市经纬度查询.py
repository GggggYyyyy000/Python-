#这个版本的街道经纬度是错误的，需要重新去补充

import requests
import json
from tqdm import tqdm
import pandas as pd
import transCoordinateSystem as trs

def b_to_w(center):
    return trs.gcj02_to_wgs84(float(center.split(",")[0]),float(center.split(",")[1]))

def data_collect(i):
        return {"adcode":i["adcode"],"level":i["level"],"name":i["name"],"lng":b_to_w(i["center"])[0],"lat":b_to_w(i["center"])[1]}

def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res

def city_location(adcode,key):
    url = "https://restapi.amap.com/v3/config/district?parameters"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"keywords": adcode,"key": key, "output": "JSON","subdistrict":"3"}
    b = requests.get(url, headers=headers, params=keyword, timeout=10)

    data = []
    if b.status_code == 200:
        html = b.text
        a = json.loads(html)["districts"][0]
        province = a["name"]
        data.append(Merge(data_collect(a),{"province":province,"city":province,"district":province,"street":province}))
        for i in a["districts"]:
            city = i["name"].replace("城区","市")
            data.append(Merge(data_collect(i),{"province":province,"city":city,"district":city,"street":city}))
            for q in i["districts"]:
                district = q["name"]
                data.append(Merge(data_collect(q),{"province":province,"city":city,"district":district,"street":district}))                
                for j in q["districts"]:
                    street = j["name"]
                    data.append(Merge(data_collect(j),{"province":province,"city":city,"district":district,"street":street}))    
        return data

def main():
    adcode = [110000, 120000, 130000, 140000, 150000, 210000, 220000, 230000, 310000, 320000, 330000, 340000, 350000, 
          360000, 370000, 410000, 420000, 430000, 440000, 450000, 460000, 500000, 510000, 520000, 530000, 540000, 
          610000, 620000, 630000, 640000, 650000, 710000, 810000, 820000]
    df = pd.DataFrame(columns=["adcode","province","city","district","street","name","lng","lat","level"])  
    key = ["53567fabaf50f1fc89fa6d17886206c6","30eb25392380a67e23ef1e67f697b316"]
    datas = []
    number = 0
    for i in tqdm(adcode):
        if len(datas) > 20000:
            number = 1
        for xx in city_location(str(i),key[number]):
                datas.append(xx)

    df = df.append(datas,ignore_index=True)
    return df
    
df = main()
df.to_csv("/Users/creative/Documents/python/工具箱/经纬度查询工具箱/中国城市经纬度.csv",encoding="utf_8_sig")



