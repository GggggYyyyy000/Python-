import requests
import json
import csv
import WGS1984

url = "https://ncov.html5.qq.com/api/getCommunityNew?province=广东省&city=广州市&district=全部&lat=28.23529&lng=112.93134"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
a = requests.get(url, headers=headers)
html = a.text
data = json.loads(html)
step1 = data["community"]["广东省"]["广州市"]
for i in step1:
    a = step1[i]
    for b in a:
        ncov1 = []
        province = b["province"]
        city = b["city"]
        district = b["district"]
        try:
            community = b["community"]
        except:
            community = "数据丢失"
        full_address = b["full_address"]
        lng_conv = b["lng"]
        lat_conv = b["lat"]
        data_conv = WGS1984.main(lng_conv,lat_conv)
        lng = data_conv[0]
        lat = data_conv[1]
        ncov1.append(province)
        ncov1.append(city)
        ncov1.append(district)
        ncov1.append(community)
        ncov1.append(full_address)
        ncov1.append(lng)
        ncov1.append(lat)
        with open("data1.csv", 'a') as f:
            write = csv.writer(f)
            write.writerow(ncov1)



