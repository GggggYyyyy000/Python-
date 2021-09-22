import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from transCoordinateSystem import bd09_to_wgs84
import re
import address_wgs1984 as ad
from tqdm import tqdm

def band_infor(link,headers):
    band = requests.get(link,headers=headers)
    if band.status_code == 200:
        htmls = band.text
        soups = BeautifulSoup(htmls,"lxml")
        try:
            name = soups.find_all(name='div',attrs={"class": "name"})[0].text
        except:
            name = "未知姓名"
        try:
            city = soups.find_all(name="div",attrs={"class":"p-text"})[0].text.replace("地区：","").replace(" ","")
        except:
            city = "未知城市"
        try:
            style = soups.find_all(name="div",attrs={"class":"p-text"})[1].text.replace(" ","").replace("风格：","")
        except:
            style = "未知风格"
        infor = {"乐队名称":name,"乐队城市":city,"乐队风格":style}
    return infor

def web_analysis(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        
        #基础信息检索
        all_data = soup.find_all(name='div',attrs={"class": "describe"})[0]
        name = all_data.find_all(name="div",attrs={"class":"title"})[0].text
        time = all_data.find_all(name="p")[0].text.replace("演出时间：","")
        livehouse = all_data.find_all(name="p")[2].text.replace("场地：","").replace(" ","")
        types = all_data.find_all(name="div",attrs={"class":"label"})[0].text
        piece = re.findall("\d+",soup.find_all(name='div',attrs={"class": "buy"})[0].find_all(name='div',attrs={"class": "price-tags"})[0].find_all(name='button')[0].text)[0]
        locat = all_data.find_all(name="p")[3].text.replace("地址：","").replace(" 查看地图","")
        a = ad.geo_address(locat,locat.rsplit('市', 1)[0])
        lng = round(a[0],6)
        lat = round(a[1],6)
        paizi = soup.find_all(name='div',attrs={"class": "sponsor clearfix"})[0].find_all(name='div',attrs={"class": "bd"})[0].text


        information = {"演出名称":name,"演出时间":time,"演出场所":livehouse,"lng":lng,"lat":lat,"演出类型":types,"价格":int(piece),"厂牌":paizi,"url":url}

        star = all_data.find_all(name="p")[1].find_all(name="a")
        band = []
        for i in star:
            link = "https://www.showstart.com" + i.attrs["href"]
            a = band_infor(link,headers)
            a.update(information)
            band.append(a)
        return band

df = pd.DataFrame(columns=["乐队名称","乐队城市","乐队风格","演出名称","演出时间","演出场所","lng","lat","演出类型","价格",
                           "厂牌","链接"])  #构建一个空表
data = []
number = 0

file_df = pd.read_excel("/Users/creative/Desktop/202108.xlsx")
for i in tqdm(range(len(file_df))):
    number += 1
    if number/100 % 1 == 0:
        time.sleep(10)
    link = file_df.loc[i,"标题链接"]

    try:
        web_data = web_analysis(link)
        for i in web_data:
            data.append(i)
    except:
        try:
            time.sleep(5)
            web_data = web_analysis(link)
            for i in web_data:
                data.append(i)
        except:
            try:
                time.sleep(5)
                web_data = web_analysis(link) 
                for i in web_data:
                    data.append(i)
            except:
                pass

df = df.append(data,ignore_index=True)
df.to_excel("/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020秋 音乐消费论文/数据收集/处理数据/2021August.xlsx") 
