import requests
import judgment
from tqdm import tqdm
import sqlite3

def data_save_mongo(words,data):
    try:
        sql = "INSERT INTO " + words + "(point_name,lng,lat,cityname,adname,address,typecode,AID)  VALUES (?,?,?,?,?,?,?,?)"
        c.executemany(sql,data)
    except:
        print("\n【运行日志】：\n警告：{}值为空值\n".format(data))

def location_conver(locations,headers):
    try:
        import json
        url = "https://restapi.amap.com/v3/assistant/coordinate/convert?parameters"
        keyword = {"locations": locations, "key": key, "coordsys": "gps"}
        b = requests.get(url, headers=headers, params=keyword, timeout=10)
        if b.status_code == 200:
            html = b.text
            json = json.loads(html)
            location = json["locations"]
            location = location.replace(";", "|")
        return location
    except:
        return locations

def json_analyse(json_file):
    import json
    with open(json_file, "r") as load_f:
        json = json.load(load_f)
    a = json["features"]
    locations = []
    for i in a:
        geometry = i["geometry"]
        coordinates = geometry["coordinates"][0]
        lefts = coordinates[0]
        left1 = str(round(lefts[0], 6))
        left2 = str(round(lefts[1], 6))
        left = left1 + "," + left2
        rights = coordinates[2]
        right1 = str(round(rights[0], 6))
        right2 = str(round(rights[1], 6))
        right = right1 + "," + right2
        location = left + "|" + right
        locations.append(location)
    print("【运行日志】：\nJSON数据分析完成\n")
    return locations

"运行日志模块"
def running_log(city,get_fail,conver_fail):
    print("\n\n【运行结果】：\n{}所有区域数据抓取完成".format(city))
    if conver_fail == []:
        print("无地球坐标转换火星坐标失败的区域")
    else:
        print("地球坐标转换火星坐标失败的区域有{}".format(conver_fail))
    if get_fail == []:
        print("无请求POI失败的区域")
    else:
        print("请求POI失败的区域有{}".format(get_fail))

if __name__ == '__main__':
    city = "440300"               #城市代码
    words = "公园"                 #检索POI的关键词
    types = "110101"                #检索POI的类型
    json_file = city + ".json"
    key = ""     #高德API的密钥（开发者权限每天3w条）
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    locations = json_analyse(json_file)
    locat = []
    conver_fail = []
    get_fail = []
    number = len(locations)
    count = 0
    print("【运行日志】：\n一共{}值需要数据转换，开始转换：".format(number))
    conn = sqlite3.connect("POI.sqlite")            #数据库储存位置
    c = conn.cursor()
    c.execute(" DROP TABLE " + words + ";")
    c.execute("CREATE TABLE " + words + "(point_name TEXT,lng real,lat real,cityname TEXT,adname TEXT,address TEXT,typecode TEXT,AID real);")

    for i in tqdm(locations):
        location = location_conver(i,headers)
        if location == i:
            conver_fail.append(location)
        else:
            locat.append(location)
            count = count + 1
    print("\n一共{}区域数据需要抓取，开始抓取：".format(count))

    for i in tqdm(locat):
        data = judgment.main(words,types,i)
        if data == i:
            get_fail.append(data)
        else:
            if data == []:
                continue
            else:
                for i in data:
                    data_save_mongo(words, i)
    conn.commit()
    running_log(city, get_fail, conver_fail)