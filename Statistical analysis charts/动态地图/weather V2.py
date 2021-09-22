import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import csv
import time
import pypinyin

def get_one_page(url):
    print('正在加载'+url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html,  "lxml")
    info = soup.find('div',  class_='wdetail')
    rows=[]
    tr_list = info.find_all('tr')[1:]       # 使用从第二个tr开始取
    for index,  tr in enumerate(tr_list):     # enumerate可以返回元素的位置及内容
        td_list = tr.find_all('td')
        dates = td_list[0].text.strip().replace("\n", "")  # 取每个标签的text信息，并使用replace()函数将换行符删除
        date1 = dates.replace('日', '').replace('月', '-').replace('年', '-')
        date = date1.split("-")[1] + "/" + date1.split("-")[2] + "/" + date1.split("-")[0]
        temperature_highs = td_list[2].text.strip().replace("\n", "").split("/")[0].strip()
        temperature_high = int(re.findall("-?\\d+", temperature_highs)[0])
        temperature_lows = td_list[2].text.strip().replace("\n", "").split("/")[1].strip()
        temperature_low = int(re.findall("-?\\d+", temperature_lows)[0])
        rows.append(list((date,  temperature_high, temperature_low)))
    print(rows)
    return rows


cities = input("请输入你要查询的城市的名称：")
city = ""
for i in pypinyin.pinyin(cities, style=pypinyin.NORMAL):
    city += "".join(i)
years = ['2019']
months = [ '06']

if __name__ == '__main__':
    with open(city +  '_weather1.csv', 'a', newline='', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'temperature_high', 'temperature_low'])
        for year in years:
            writer.writerow(year+city)
            for month in months:
                url = 'http://www.tianqihoubao.com/lishi/' + city + '/month/' + year + month + '.html'
                html = get_one_page(url)
                content = parse_one_page(html)
                writer.writerows(content)
                print(city + year + month + ' is OK!')
                time.sleep(2)


