import requests
import re
import sqlite3
from bs4 import BeautifulSoup
import pypinyin


def page_url(word):
    element = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        element += "".join(i)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    for year in years:
        for month in months:
            url = 'http://www.tianqihoubao.com/lishi/' + element + '/month/' + year + month + '.html'
            b = requests.get(url,headers=headers)
            if b.status_code==200:
                html = b.text
                print("正在爬取{}年{}月天气数据".format(year,month))
                data_down(html)


def data_down(html):
    soup = BeautifulSoup(html,"lxml")
    info = soup.find('div', class_='wdetail')
    weather_data = []
    tr_list = info.find_all('tr')[1:]  # 使用从第二个tr开始取
    for index, tr in enumerate(tr_list):  # enumerate可以返回元素的位置及内容
        td_list = tr.find_all('td')
        dates = td_list[0].text.strip().replace("\n", "")  # 取每个标签的text信息，并使用replace()函数将换行符删除
        date = dates.replace('日','').replace('月','-').replace('年','-')
        weather = td_list[1].text.strip().replace("\n", "").split("/")[0].strip()
        temperature_highs = td_list[2].text.strip().replace("\n", "").split("/")[0].strip()
        temperature_high = int(re.findall("-?\\d+",temperature_highs)[0])
        temperature_lows = td_list[2].text.strip().replace("\n", "").split("/")[1].strip()
        temperature_low = int(re.findall("-?\\d+",temperature_lows)[0])
        weather_data.append(list((date, weather, temperature_high, temperature_low)))
    save_data(weather_data)


def save_data(weather_data):
    sql = "INSERT INTO cs_weather_data(日期, 天气状况, 最高温度, 最低温度)  VALUES (?,?,?,?)"
    c.executemany(sql,weather_data)


if __name__ == '__main__':
    years = ['2011','2012', '2013', '2014', '2015', '2016', '2017', '2018']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    word = input("请输入你要查询的城市的名称：")
    conn = sqlite3.connect("E:\\Python\\creeper_data.db")
    c = conn.cursor()
    page_url(word)
    conn.commit()
    print("2011-2018年{}天气情况成功写入数据库".format(word))