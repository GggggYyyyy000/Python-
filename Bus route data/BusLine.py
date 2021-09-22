import requests
import json
import csv
import random
import time
import WGS1984
import citybus
import conversion_geo
import os
import pandas as pd
from tqdm import tqdm

def station(html,keywords,bus_station,buslines_information,buslines_polyline,city):
    buslines = html["buslines"]
    count = 0
    for i in buslines:
        count = count+1
        busstops = i["busstops"]
        """站点信息"""
        for T in busstops:
            cell = []
            lng1 = T["location"].split(",")[0]
            lat1 = T["location"].split(",")[1]
            cell = [city,T["name"],WGS1984.main(lng1,lat1)[0],WGS1984.main(lng1, lat1)[1],T["id"],i["name"],count]
            with open(bus_station, 'a',newline='', encoding='utf-8') as f:
                write = csv.writer(f)
                write.writerow(cell)

        """线路信息"""
        information = [city,count,keywords[0:4],i["name"],i["basic_price"],i["total_price"],i["distance"],i["start_stop"],i["end_stop"],i["type"],i["start_time"],i["end_time"]]
        with open(buslines_information, 'a',newline='', encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(information)

        """线路路线"""
        polyline = i["polyline"]
        split_polyline = polyline.split(";")
        cou = 0
        buslines_name2 = i["name"]
        for i in split_polyline:
            cou = cou + 1
            excessive = i.split(",")
            bus_polyline = [city,cou,buslines_name2,keywords[0:4],WGS1984.main(excessive[0],excessive[1])[0],WGS1984.main(excessive[0],excessive[1])[1]]
            with open(buslines_polyline, 'a',newline='', encoding='utf-8') as f:
                write = csv.writer(f)
                write.writerow(bus_polyline)

def research(city,keywords,key,bus_station,buslines_information,buslines_polyline):
    url = "https://restapi.amap.com/v3/bus/linename?parameters"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"s": "rsv3", "extensions": "all", "key": key, "output": "json", "city": city, "offset": "2","keywords": keywords, "platform": "JS"}
    a = requests.get(url, headers=headers, params=keyword)
    html = a.text
    data = json.loads(html)
    if data["status"] == "1":
        station(data, keywords,bus_station,buslines_information,buslines_polyline,city)
    else:
        print("未查询到{}市的{}信息".format(city,keywords))



def main(city,key,province):
    if os.path.isdir(os.getcwd()+"/data")==False:
        os.mkdir(os.getcwd()+"/data")
    if os.path.isdir(os.getcwd()+"/data/" + province)==False:
        os.mkdir(os.getcwd()+"/data/" + province)

    now_path = os.getcwd()+"/data/" + province + "/csv/"
    if os.path.isdir(now_path)==False:
        os.mkdir(now_path)

    bus_station = now_path + city + "公交站点.csv"
    buslines_information = now_path + city + "公交线路信息.csv"
    buslines_polyline = now_path + city + "公交线路.csv"

    with open(bus_station, 'a',newline='', encoding='utf_8_sig') as f:
        write = csv.writer(f)
        write.writerow(["城市","站点名称","lng","lat","id","name","正反线路"])

    with open(buslines_information, 'a',newline='', encoding='utf_8_sig') as f:
        write = csv.writer(f)
        write.writerow(["城市","正反线路","简称","全称","上车票价","全程票价","距离","起点站","终点站","线路类型","首班时间","末班时间"])

    with open(buslines_polyline, 'a',newline='', encoding='utf_8_sig') as f:
        write = csv.writer(f)
        write.writerow(["城市","序号","全称","简称","lng","lat"])

    citybus_name = citybus.main(city)
    """
    df = pd.read_excel("/Users/creative/Documents/python/Bus route data/dtt.xlsx")
    citys = df[df["字段1"] == city]
    citys = citys.reset_index()
    citybus_name = []
    for i in range(len(citys)):
        citybus_name.append({"city":city,"name":citys.loc[i,"字段2"]})
    """

    print("【正在获取{}公交线路数据】\n".format(city))

    for i in tqdm(citybus_name):
        keywords = i["name"]
        city = i["city"]
        research(city,keywords,key,bus_station,buslines_information,buslines_polyline)
        time.sleep(random.randint(0,1))
    
    conversion_geo.main(bus_station,buslines_information,buslines_polyline,city,province)

key = "559bdffe35eec8c8f4dae959451d705c"
province = "福建省"
city = "厦门"  


main(city,key,province)