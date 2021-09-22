import requests
import json
import pandas as pd
import WGS1984

def geo_address(address,city):
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    key = "a28ef383f88985aa56506869dac72b7e"
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
    key = "a28ef383f88985aa56506869dac72b7e"
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




