import requests
import json
from tqdm import tqdm
import pandas as pd
import transCoordinateSystem as trs

def geo_address(location,coord_type):
    if coord_type == "wgs84":
        lo = trs.wgs84_to_gcj02(location.split(",")[0],location.split(",")[1])
        location = str(lo[0]) + "," + str(lo[1])
    if coord_type == "bd09ll":
        lo = trs.bd09_to_gcj02(location.split(",")[0],location.split(",")[1])
        location = str(lo[0]) + "," + str(lo[1])

    url = "https://restapi.amap.com/v3/geocode/regeo?parameters"
    key = "53567fabaf50f1fc89fa6d17886206c6"
    zxs = ["北京市","上海市","天津市","重庆市"] #直辖市名单
    sxx = ["济源市""仙桃市","潜江市","天门市","神农架林区","五指山市","文昌市","琼海市",
            "万宁市","东方市","定安县","屯昌县","澄迈县","临高县","琼中黎族苗族自治县",
            "保亭黎族苗族自治县","白沙黎族自治县","昌江黎族自治县","乐东黎族自治县","陵水黎族自治县",
            "阿拉尔市","图木舒克市","五家渠市","北屯市","铁门关市","双河市","可克达拉市"] #省辖县名单

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"location": location,"key": key, "output": "JSON"}
    b = requests.get(url, headers=headers, params=keyword, timeout=10)

    if b.status_code == 200:
        html = b.text
        a = json.loads(html)["regeocode"]["addressComponent"]
        infors = {"province":a["province"],
                  "city":a["city"],
                  "district":a["district"],
                  "township":a["township"]}

        if infors["province"] in zxs: #判断是不是直辖市
            infors["city"] = infors["province"]
        if infors["district"] in sxx: #判断是不省辖县
            infors["city"] = infors["district"]    
        try:
            infors["businessAreas"] = a["businessAreas"][0]["name"]
        except:
            infors["businessAreas"] = ""

    return infors

files = pd.read_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/【暂停】2020秋 音乐消费论文/数据收集/处理数据/band_all.xlsx")

for i in tqdm(range(len(files))):
    location = str(files.loc[i,"lng"]) + "," + str(files.loc[i,"lat"])
    try:
        infor = geo_address(location,"wgs1984")
        files.loc[i,"province"] = infor["province"]
        files.loc[i,"city"] = infor["city"]
        files.loc[i,"district"] = infor["district"]
        files.loc[i,"township"] = infor["township"]
        files.loc[i,"businessAreas"] = infor["businessAreas"]
    except:
        pass

files.to_csv("/Users/creative/Desktop/band_all.csv",encoding="utf_8_sig")
    





