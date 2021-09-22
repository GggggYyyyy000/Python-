import geopandas as gpd
import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
import requests
from ChineseAdminiDivisionsDict import CitiesCode, ProvinceCode
import os

data = "weihai_busline.shp"
data_path = os.getcwd()+"/data/" + "山东" + "/shp/line/"
busline = gpd.read_file(data_path + data)

def boundary_judgment(city):
    url = "https://geo.datav.aliyun.com/areas/bound/geojson?code={}".format(CitiesCode[str(city)])
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    a = requests.get(url, headers=headers)
    datas = gpd.read_file(a.text, ensure_ascii=False)
    boundary = datas.drop(list(datas.columns[[0,2,3,4,5]]),axis=1)
    return boundary

city = "威海"
city_boundary = boundary_judgment(city)
city_boundary.plot()

plt.show