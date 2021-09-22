import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import re
from transCoordinateSystem import bd09_to_wgs84,wgs84_to_bd09


def house_find(id):
    url = "https://sz.ke.com/xiaoqu/rs" + str(id) + "/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(url,headers=headers)

    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        urls = soup.find_all(name='div',attrs={"class": "title"})[1].find_all(name='a')[0]["href"]
        c = requests.get(urls,headers=headers,timeout=10)
        if c.status_code == 200:
            html2 = c.text
            soup2 = BeautifulSoup(html2, 'lxml')
            xx = soup2.find_all(name='div',attrs={"class": "xiaoquInfo"})[0].text
            house = int(re.findall(r'(.*?)户',xx)[0])
            return house

df1 = pd.read_excel("/Users/creative/Desktop/寻找户数.xlsx")

for i in tqdm(range(len(df1))):
    name = df1.loc[i,"name_2"] 
    try:
        df1.loc[i,"house_number"] = house_find(name)
    except:
        df1.loc[i,"house_number"] = "无结果"
    

df1.to_excel("/Users/creative/Desktop/寻找户数结果.xlsx") 

    
    
    

        