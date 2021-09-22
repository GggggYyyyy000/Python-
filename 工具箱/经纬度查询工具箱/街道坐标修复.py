import requests
import json
from tqdm import tqdm
import pandas as pd
import transCoordinateSystem as trs

def b_to_w(center):
    return trs.gcj02_to_wgs84(float(center.split(",")[0]),float(center.split(",")[1]))

def fix_street(street,city,key):
    url = "https://restapi.amap.com/v3/place/text?parameters"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"keywords": street+"政府", "key": key, "city": city,"types":"乡镇级政府及事业单位","citylimit":"true"}
    b = requests.get(url, headers=headers, params=keyword)
    if b.status_code == 200:
        a = b_to_w(json.loads(b.text)["pois"][0]["location"])
        a.append(json.loads(b.text)["pois"][0]["name"])
    return a

df = pd.read_csv("/Users/creative/Documents/python/工具箱/经纬度查询工具箱/中国城市经纬度.csv")


for i in tqdm(range(len(df))):
    if i > 20000:
        key = "53567fabaf50f1fc89fa6d17886206c6"
    else:
        key = "30eb25392380a67e23ef1e67f697b316"
    if df.loc[i,"level"] == "street":
        street = df.loc[i,"name"]
        city = df.loc[i,"adcode"]
        try:
            location = fix_street(street,city,key)
            df.loc[i,"lng"] = location[0]
            df.loc[i,"lat"] = location[1]
            df.loc[i,"exam"] = location[2]
        except:
            pass

df.to_csv("/Users/creative/Documents/python/工具箱/经纬度查询工具箱/test2.csv",encoding="utf_8_sig")



