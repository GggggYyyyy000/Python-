import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import re
from transCoordinateSystem import bd09_to_wgs84,wgs84_to_bd09

def page_analysis(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find_all(name='p',attrs={"class": "content__title"})[0].text.replace(" ","").replace("\n","")
        longitude = float(re.findall(r'longitude:.*?(?=,)', str(soup))[0].replace("longitude: ","").replace("'",""))
        latitude = float(re.findall(r'latitude:.*', str(soup))[0].replace("latitude: ","").replace("'",""))
        price = soup.find_all(name='div',attrs={"class": "content__aside--title"})[0].find_all(name='span')[0].text
        floor = soup.find_all(name='li',attrs={"class": "floor"})[0].find_all(name='span',attrs={"class": ""})[0].text
        types = soup.find_all(name='ul',attrs={"class": "content__aside__list"})[0].find_all(name='li')[0].text.replace("租赁方式：","")
        area =   soup.find_all(name='ul',attrs={"class": "content__aside__list"})[0].find_all(name='li')[1].text.replace("房屋类型：","")
        area = float(re.findall(r"卫(.*?)㎡",area)[0].replace("卫","").replace("㎡",""))
        house_data = {"name":name,"price":price,"floor":floor,"area":area,"types":types,"lng":bd09_to_wgs84(longitude,latitude)[0],"lat":bd09_to_wgs84(longitude,latitude)[1]}
        return(house_data)


das = []    
df = pd.DataFrame(columns=["name","price","floor","area","types","lng","lat"])  

url_df = pd.read_csv("/Users/creative/Documents/python/Web_Creeper/房价数据爬取/租房信息链接.csv")

for i in tqdm(range(len(url_df))):
    url = url_df.loc[i,"url"]
    if "zufang" in url:
        das.append(page_analysis(url))

df = df.append(das,ignore_index=True)
df.to_excel("/Users/creative/Documents/python/Web_Creeper/房价数据爬取/house_price.xlsx") 


