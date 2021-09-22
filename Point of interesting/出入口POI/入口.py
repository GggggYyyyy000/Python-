import requests
import WGS1984
import pandas as pd


"""这个模块是POI信息检索"""
def poi_get(types,locat,key,parent):
    try:
        page = 0
        all_data = []
        for i in range(0,5):
            page = page + 1
            url = "https://restapi.amap.com/v3/place/polygon?parameters"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
            keyword = {"types": types, "key": key, "polygon": locat,"extensions":"all","page": page}
            b = requests.get(url, headers=headers, params=keyword, timeout=10)
            if b.status_code == 200:
                import json
                html = b.text
                print("正在检索第{}页的数据".format(page))
                json = json.loads(html)["pois"]
                for i in json:
                    if i["parent"] == parent:
                        a = i["location"].split(",")
                        b = WGS1984.main(a[0], a[1])

                        data = {"id":i["id"],"parent":i["parent"],"name":i["name"],"childtype":i["childtype"],
                            "lat":b[1],"lng":b[0]}
                    
                        all_data.append(data)
        return all_data 
    except:
        print("数据检索失败")      

     
df = pd.DataFrame(columns=["id","parent","name","childtype","lat","lng"])  #构建一个空表

types = "990000"
locat = "113.942567,22.519253|113.958746,22.502086" #检索区域的范围，高德坐标拾取器矩形左上右下坐标
key = "a28ef383f88985aa56506869dac72b7e" #高德API密钥
parent = "B0FFI1VATT"

all_data = poi_get(types,locat,key,parent)  #运行主程序
for i in all_data:
    df = df.append(i,ignore_index=True) 
df.to_excel("990000.xlsx")