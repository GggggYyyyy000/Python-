import tkinter
import requests
import json
import csv
import WGS1984

def data(province,city):
    url = "https://ncov.html5.qq.com/api/getCommunityNew?parameters"
    keyword = {"province":province,"city": city, "district": "全部", "lat": "23.096076","lng":"113.297195"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    a = requests.get(url, headers=headers,params=keyword)
    html = a.text
    data = json.loads(html)
    step1 = data["community"][province][city]
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
            with open("data.csv", 'a') as f:
                write = csv.writer(f)
                write.writerow(ncov1)

win = tkinter.Tk()
win.title("WSSD设计")
win.geometry("400x60+400+400")
entry = tkinter.Entry(win,width = 30)
entry.insert(10,"请输入想要查询的城市：如湖南省长沙市")
def func1(event):
    entry.delete(0,20)
entry.bind("<Button-1>",func1)
def func2():
    url = entry.get()
    province = url[0:3]
    city = url[-3:]
    data(province,city)
button = tkinter.Button(win,text="确定", command = func2,width = 6,height = 1)
entry.pack()
button.pack()
win.mainloop()