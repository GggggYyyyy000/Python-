import requests
import json
import time
import geopandas as gpd
import geo_boundary
from tqdm import tqdm
import pandas as pd
from transCoordinateSystem import bd09_to_wgs84,wgs84_to_bd09


def point_information(file_path):
    point_df = pd.read_csv(file_path)
    pinf = []
    for i in range(len(point_df)):
        lo = wgs84_to_bd09(point_df.loc[i,"x"],point_df.loc[i,"y"])
        location = str(round(lo[1],6)) + "," + str(round(lo[0],6))
        pinf.append({"location":location,"radius":point_df.loc[i,"radius"]}) 
    return pinf

def judgeBaiduApi(location, page_num, radius):
    URL = "http://api.map.baidu.com/place/v2/search?"
    key = "i9av91KEX5DP6dDdByUFwmp2MjQMX9kl"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"query": "医院", "ak": key, "output": "json","location":location,"radius":radius,
               "scope":"2","page_size":"20","page_num":page_num,"radius_limit":"false"}
    b = requests.get(URL, headers=headers, params=keyword)
    if b.status_code == 200:
        html = b.text
        number = json.loads(html)["total"]
    return number

def requestBaiduApi(location, page_num, radius):
    URL = "http://api.map.baidu.com/place/v2/search?"
    key = "i9av91KEX5DP6dDdByUFwmp2MjQMX9kl"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"query": "医院", "ak": key, "output": "json","location":location,"radius":radius,
               "scope":"2","page_size":"20","page_num":page_num,"radius_limit":"false"}
    b = requests.get(URL, headers=headers, params=keyword)
    if b.status_code == 200:
        html = b.text
        data = json.loads(html)["results"]
        datas =[]
        for i in data:
            try:
                datas .append(  {"name":i["name"],"area":i["area"],"address":i["address"],"uid":i["uid"],
                        "tag":i["detail_info"]["tag"],"url":i["detail_info"]["detail_url"],
                        "lng":bd09_to_wgs84(float(i["location"]["lng"]),float(i["location"]["lat"]))[0],
                        "lat":bd09_to_wgs84(float(i["location"]["lng"]),float(i["location"]["lat"]))[1]})
            except:
                datas .append(  {"name":i["name"],"area":i["area"],"address":"NULL","uid":i["uid"],
                        "tag":"NULL","url":"NULL",
                        "lng":bd09_to_wgs84(float(i["location"]["lng"]),float(i["location"]["lat"]))[0],
                        "lat":bd09_to_wgs84(float(i["location"]["lng"]),float(i["location"]["lat"]))[1]})
        return datas    

file_path = "/Users/creative/Desktop/point.csv"
pinf = point_information(file_path)
ddt = []
page_num = "0"

try:
    for i in tqdm(pinf):
        location = i["location"]
        radius = i["radius"]
        judge = judgeBaiduApi(location, page_num, radius)
        if int(int(judge)/20) >= 1:
            page = int(int(judge)/20)
            for i in range(0,page+1):
                for x in requestBaiduApi(location,str(i),radius):
                    ddt.append(x)      
        else:
            for x in requestBaiduApi(location,page_num,radius):
                    ddt.append(x)  
except:
    import time
    time.sleep(2)
    for i in tqdm(pinf):
        location = i["location"]
        radius = i["radius"]
        judge = judgeBaiduApi(location, page_num, radius)
        if int(int(judge)/20) >= 1:
            page = int(int(judge)/20)
            for i in range(0,page+1):
                for x in requestBaiduApi(location,str(i),radius):
                    ddt.append(x)      
        else:
            for x in requestBaiduApi(location,page_num,radius):
                    ddt.append(x)  

df = pd.DataFrame(columns=["name","area","lng","lat","address","uid","tag","url"])  
df = df.append(ddt,ignore_index=True)


df.to_excel("医院datas.xlsx") 

 
