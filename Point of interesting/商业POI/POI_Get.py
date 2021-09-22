import requests
import WGS1984
import pandas as pd

"""这个模块是详情POI检索模块"""
def id_get(cpid,key,headers):
    try:
        url = "https://restapi.amap.com/v3/place/detail?parameters"
        keyword = {"id": cpid, "key": key, "output": "JSON"}
        b = requests.get(url, headers=headers, params=keyword, timeout=10)
        if b.status_code == 200:
            import json
            html = b.text
            json = json.loads(html)["pois"][0]
            if json["biz_ext"]["rating"] == []:
                rating = "0"
            else:
                rating = json["biz_ext"]["rating"]
            data = {"mall_name":json["name"],"mall_type":json["type"],"mall_typecode":json["typecode"],"mall_rating":rating}
        return data
    except:
        print("mall信息检索失败")

"""这个模块是POI信息检索"""
def poi_get(types,locat,key):
    try:
        page = 0
        all_data = []
        for i in range(0,100):
            page = page + 1
            url = "https://restapi.amap.com/v3/place/polygon?parameters"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
            keyword = {"keywords": types, "key": key, "polygon": locat,"extensions":"all","page": page}
            b = requests.get(url, headers=headers, params=keyword, timeout=10)
            if b.status_code == 200:
                import json
                html = b.text
                print("正在检索第{}页的数据".format(page))
                json = json.loads(html)["pois"]
                for i in json:
                    if i["indoor_map"] == "1":   
                        a = i["location"].split(",")
                        b = WGS1984.main(a[0], a[1])
                        if i["address"] == []:
                            address = "[]"
                        else:
                            address = i["address"]
                        if i["biz_ext"]["rating"] == []:
                            rating = "0"
                        else:
                            rating = i["biz_ext"]["rating"]
                        cpid = i["indoor_data"]["cpid"]
                        data = {"id":i["id"],"name":i["name"],"pname":i["pname"],"cityname":i["cityname"],
                            "adname":i["adname"],"address":address,"lat":b[1],"lng":b[0],"rating":rating,
                            "type":i["type"],"typecode":i["typecode"],"cpid":cpid,
                            "floor":i["indoor_data"]["floor"],"truefloor":i["indoor_data"]["truefloor"]}
                        Supplementary_data = id_get(cpid,key,headers)
                        all_data.append(dict(data,**Supplementary_data))
        return all_data 
    except:
        print("数据检索失败")      

     
df = pd.DataFrame(columns=["id","name","pname","cityname","adname","address","lat","lng","rating","type",
                           "typecode","cpid","floor","truefloor","mall_name","mall_type","mall_typecode",
                           "mall_rating"])  #构建一个空表

types = "餐饮服务|风景名胜|公司企业|购物服务|交通设施服务|金融保险服务|科教文化服务|商务住宅|生活服务|体育休闲服务|政府机构及社会团体|医疗保健服务|公共设施|住宿服务|室内设施|通行设施|道路附属设施|事件活动|汽车服务|汽车维修|汽车销售|摩托车服务|地名地址信息"
locat = "113.934178,22.51908|113.939854,22.515432" #检索区域的范围，高德坐标拾取器矩形左上右下坐标
key = "a28ef383f88985aa56506869dac72b7e" #高德API密钥
all_data = poi_get(types,locat,key)  #运行主程序
for i in all_data:
    df = df.append(i,ignore_index=True) #将数据填入到空表中
df.to_excel("shopping_mall.xlsx") #保存excel

"""可以继续优化的方向：
   01:对矩形区域进行分割，获取更加细密度的POI
   02:对key进行多个Key值填入，防止程序因权限不足而死机"""