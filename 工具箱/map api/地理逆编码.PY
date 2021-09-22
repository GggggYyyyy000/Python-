import requests
import json
import pandas as pd
import WGS1984

def geo_address(address,city):
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    key = "21f808ea634227cd00bcb4459a62c5c3"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"address": address,"city":city, "key": key, "output": "JSON"}
    b = requests.get(url, headers=headers, params=keyword, timeout=10)
    if b.status_code == 200:
        html = b.text
        a = json.loads(html)["geocodes"][0]
        location = a["location"].split(',')
        b = WGS1984.main(location[0], location[1])
        lng = b[0]
        lat = b[1]
    return lng,lat

def poi_query(name,city):
    url = "https://restapi.amap.com/v3/place/text?parameters"
    key = "21f808ea634227cd00bcb4459a62c5c3"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    keyword = {"keywords": name, "key": key, "city": city}
    b = requests.get(url, headers=headers, params=keyword)
    if b.status_code == 200:
        import json
        html = b.text
        json = json.loads(html)["pois"][0]
        #print(json)
        a = json["location"].split(",")
        
        b = WGS1984.main(a[0], a[1])
        lng = b[0]
        lat = b[1]
    return lng,lat


df = pd.read_excel("/Users/creative/Desktop/深圳市医院.xlsx",sheet_name="Sheet2") 
city = "深圳"
data = []
for i in range(len(df)):
    name = df.loc[i,"机构名称"]  
    address = df.loc[i,"地址"]  
    print(name)
    try:
        #address = poi_query(name,city)
        address = geo_address(address,city)
        infor = {"name":name,"lng":address[0],"lat":address[1]}
    except:
        infor = {"name":name,"lng":0,"lat":1}
    data.append(infor)

dff = pd.DataFrame(columns=["name","lng","lat"]) 
dff = dff.append(data,ignore_index=True)
dff.to_csv("data2.csv") 

        






#address = geo_address(address,city)
#print(address)

