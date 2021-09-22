import requests
import WGS1984

def judgment(key,words,types,locat,headers):
    import json
    URL = "https://restapi.amap.com/v3/place/polygon?parameters "
    keyword = {"keywords": words, "key": key, "type": types, "polygon": locat}
    b = requests.get(URL, headers=headers, params=keyword, timeout=10)
    if b.status_code == 200:
        html = b.text
        mm = json.loads(html)
        a = mm["pois"]
        x = len(a)
    return x

def poi_get1(key,words,types,locat,headers):
    try:
        import json
        URL = "https://restapi.amap.com/v3/place/polygon?parameters "
        keyword = {"keywords": words, "key": key, "type": types, "polygon": locat}
        b = requests.get(URL, headers=headers, params=keyword, timeout=10)
        if b.status_code == 200:
            html = b.text
            json = json.loads(html)
            try:
                a = json["pois"]
                datas = []
                for i in a:
                    data = []
                    name = i["name"]
                    data.append(name)
                    location = i["location"]
                    a = location.split(",")
                    b = WGS1984.main(a[0],a[1])
                    lng = b[0]
                    lat = b[1]
                    data.append(lng)
                    data.append(lat)
                    cityname = i["cityname"]
                    data.append(cityname)
                    adname = i["adname"]
                    data.append(adname)
                    address = i["address"]
                    if address == []:
                        address = "未查询到地址"
                    else:
                        address = i["address"]
                    data.append(address)
                    typecode = i["typecode"]
                    data.append(typecode)
                    AID = i["id"]
                    data.append(AID)
                    datas.append(data)
                return datas
            except:
                print("\n【运行日志】：\n该区域缺少{}的相关POI".format(words))
                print(json)
    except:
        return locat

def poi_get2(key,words,types,locat,headers):
    try:
        page = 0
        result = []
        import json
        for i in range(0,101):
            page = page + 1
            key = "a7e8a666ad7995853d8657fde9fa52c5"
            URL = "https://restapi.amap.com/v3/place/polygon?parameters "
            keyword = {"keywords": words, "key": key, "type": types, "polygon": locat, "page": page}
            b = requests.get(URL, headers=headers, params=keyword, timeout=10)
            if b.status_code == 200:
                html = b.text
                mm = json.loads(html)
                try:
                    a = mm["pois"]
                    datas = []
                    for i in a:
                        data = []
                        name = i["name"]
                        data.append(name)
                        location = i["location"]
                        a = location.split(",")
                        b = WGS1984.main(a[0], a[1])
                        lng = b[0]
                        lat = b[1]
                        data.append(lng)
                        data.append(lat)
                        cityname = i["cityname"]
                        data.append(cityname)
                        adname = i["adname"]
                        data.append(adname)
                        address = i["address"]
                        if address == []:
                            address = "未查询到地址"
                        else:
                            address = i["address"]
                        data.append(address)
                        typecode = i["typecode"]
                        data.append(typecode)
                        AID = i["id"]
                        data.append(AID)
                        datas.append(data)
                    result.append(datas)
                except:
                    print("\n【运行日志】：\n该区域缺少{}的相关POI".format(words))
                    print(json)
        return result
    except:
        return locat

def main(words,types,locat):
    key = "a7e8a666ad7995853d8657fde9fa52c5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = judgment(key,words,types,locat,headers)
    if b < 19:
        a = []
        data = poi_get1(key,words,types,locat,headers)
        a.append(data)
    else:
        a = poi_get2(key,words,types,locat,headers)
    return a