import requests
from bs4 import BeautifulSoup

def information_get(base_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(base_url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        link = soup.find_all(name='a',attrs={"class": "g-name a-link"})
        for i in link:
            links = i.attrs['href']
            band = requests.get(links,headers=headers)
            if band.status_code == 200:
                htmls = band.text
                soups = BeautifulSoup(htmls,"lxml")
                try:
                    name = soups.find_all(name='div',attrs={"class": "name"})[0].text
                except:
                    name = "未知姓名"
                try:
                    city = soups.find_all(name="ol",attrs={"class":"dec"})[0].li.text.replace("地区：","").replace(" ","")
                except:
                    city = "未知城市"
                try:
                    style = soups.find_all(name="ol",attrs={"class":"dec"})[0].find_all(name='li')[1].text.replace(" ","").replace("\n","").replace("风格：","").replace("\t","")
                except:
                    style = "未知风格"
                infor = {"name":name,"city":city,"style":style}
                print(infor)
                data.append(infor)
        return data
        
df = pd.DataFrame(columns=["name","city","style"])
base_url = "https://www.showstart.com/artist/list?pageNo="
a = 0
for i in range(1,1521):
    a = a + 1
    url = base_url + str(a)
    data = information_get(url)
    df = df.append(data,ignore_index=True)

df.to_excel("band_list.xlsx")



