import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

def house_information(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
    
    try:
        price1 = int(soup.find_all(name='strong')[0].text)
        price2 = int(soup.find_all(name='strong')[1].text)
    except:
        price1 = "无数据"
        price2 = "无数据"

    return {"community":soup.find_all(name='a',attrs={"class": "blue-14"})[0].text,                                      # 社区名称
        "all_price(万元)":price1,
        "gov_price(/㎡)":price2,
        "area(㎡)":soup.find_all(name='li',attrs={"class": "two"})[0].find_all(name="strong")[0].text.replace("㎡","") ,  #面积
        "number":soup.find_all(name='li',attrs={"class": "one"})[0].find_all(name="strong")[0].text ,                    #几房
        "fitment":soup.find_all(name='li',attrs={"class": "three"})[1].find_all(name="p")[0].text ,                      #装修情况
        "type":soup.find_all(name='li',attrs={"class": "two"})[0].find_all(name="p")[0].text,
        "floor":soup.find_all(name='li',attrs={"class": "one"})[0].find_all(name="p")[0].text.split("/")[0],             #该户型所在层数
        "all_floor":soup.find_all(name='li',attrs={"class": "one"})[0].find_all(name="p")[0].text.split("/")[1],         #本栋楼总层数
        "direction":soup.find_all(name='li',attrs={"class": "three"})[1].find_all(name="strong")[0].text,                #方向
        "address":soup.find_all(name='div',attrs={"class": "esf-info-box b-b-dc fix otherinfo f14"})[0].find_all("p")[1].text.replace("所在地址：","").replace(" 查看地图","")}

page= 1
data = []
for i in tqdm(range(0,2)): #构建页面
    page += 1 
    page_url = "http://zf.szhome.com/Search.html?sor=1&aom=1&kwd=&xzq=0&pq=0&price=0&prif=0&prit=0&barea=0&baf=0&bat=0&hx=0&ord=0&dtyx=0&dtst=0&scat=0&sx=0&schid=0&page=" + str(page)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(page_url,headers=headers)
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        url_database = soup.find_all(name='div',attrs={"class": "lpinfo"})

        #分页面数据爬取
        for i in url_database:
            url = "http://zf.szhome.com" + i.find_all("a")[0].attrs["href"]
            data.append(house_information(url))


df = pd.DataFrame(columns=["community","all_price(万元)","gov_price(/㎡)","area(㎡)","number","fitment","type","floor","all_floor","direction",
                           "address"])  #构建一个空表

df = df.append(data,ignore_index=True)  #数据保存
df.to_excel("data.xlsx") 