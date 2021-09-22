import requests
from bs4 import BeautifulSoup
import pandas as pd

def information_get(base_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(base_url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        link = soup.find_all(name='a',attrs={"class": "name col-333"})
        for i in link:
            links = i.attrs['href']
            LABEL = requests.get(links,headers=headers)
            if LABEL.status_code == 200:
                htmls = LABEL.text
                soups = BeautifulSoup(htmls,"lxml")
                try:
                    name = soups.find_all(name='div',attrs={"class": "name"})[0].text
                except:
                    name = "未知姓名"
                try:
                    city = soups.find_all(name="ol",attrs={"class":"dec"})[0].li.text.replace("城市：","").replace(" ","")
                except:
                    city = "未知城市"
                infor = {"name":name,"city":city}
                print(infor)
                data.append(infor)
        return data
        
df = pd.DataFrame(columns=["name","city"])
base_url = "https://www.showstart.com/host/list?pageNo="
a = 0
for i in range(1,166):
    a = a + 1
    url = base_url + str(a)
    data = information_get(url)
    df = df.append(data,ignore_index=True)
#166
df.to_excel("LABEL_list.xlsx")



