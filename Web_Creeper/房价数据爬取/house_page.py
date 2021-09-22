import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from pandas.core.frame import DataFrame
import pandas as pd
import re
from transCoordinateSystem import bd09_to_wgs84,wgs84_to_bd09


def page_list():
    url = "https://sz.zu.ke.com/zufang/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    b = requests.get(url,headers=headers)
    data = []
    if b.status_code == 200:
        html = b.text
        soup = BeautifulSoup(html, 'lxml')
        ax = soup.find_all(name='li',attrs={"class": "filter__item--level2","data-type":"district"})
        del ax[0]
        for i in ax:
            dis_area = "https://sz.zu.ke.com" + i.find_all(name="a")[0]["href"]
            c = requests.get(dis_area,headers=headers)
            if c.status_code == 200:
                htmlc = c.text
                soupc = BeautifulSoup(htmlc, 'lxml')
                judge = soupc.find_all(name='li',attrs={"class": "filter__item--level3"})
                del judge[0]
                for ii in judge:
                    print(ii)
                    common_area = "https://sz.zu.ke.com" + ii.find_all(name="a")[0]["href"]
                    d = requests.get(common_area,headers=headers)
                    if d.status_code == 200:
                        htmld = d.text
                        soupd = BeautifulSoup(htmld, 'lxml')
                        common_judge = int(soupd.find_all(name='span',attrs={"class": "content__title--hl"})[0].text)/30
                        for page in range(int(common_judge)+1):
                            page_url = common_area + "pg" + str(page) + "/#contentList"
                            e = requests.get(page_url,headers=headers)
                            if e.status_code == 200:
                                htmle = e.text
                                soupe = BeautifulSoup(htmle, 'lxml')
                                ax2 = soupe.find_all(name='div',attrs={"class": "content__list--item"})
                                for urlx in ax2:
                                    urls = "https://sz.zu.ke.com" + urlx.find_all(name='a')[0]["href"]
                                    print(urls)
                                    data.append(urls)
    return data

data = {"url":page_list()}
datas= DataFrame(data)
print(len(datas))

datas.to_csv("租房信息链接.csv",encoding="utf_8_sig")
