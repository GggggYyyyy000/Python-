import json
import geopandas as gpd
import pandas as pd
import WGS1984
import requests
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r * 1000

def get_G(x):#距离衰减计算公式
    if x <= 1098:
        G = (np.exp(-0.5 * (x/1098)**2) - np.exp(-0.5)) / (1-np.exp(-0.5))
        return G
    else:
        return 0

def get_Rj(x):#$R_{j}$ 计算
    x = x.reset_index()
    sj = x['医生'][0] #供给点的衡量指标，如公园的面积
    dt = 0
    for i in range(len(x)):
        vl = x['pop'][i] * get_G(x['length'][i]) #需求点的衡量指标，如小区的人数
        dt += vl
    return sj/dt

def get_A(x):#$A_{i}$ 计算
    x = x.reset_index()
    dt = 0
    for i in range(len(x)):
        vl = x['vl_R'][i] * get_G(x['length'][i])
        dt += vl
    return dt

def step01(supply_df,demand_df):
    #第一步计算
    #对学校进行缓冲
    supply_copy = supply_df.copy() 
    supply_copy['geometry'] = supply_copy['geometry'].buffer(1098) 
    supply_copy = gpd.sjoin(supply_copy,demand_df,op='contains') #建立空间连接，将在缓冲区内的小区连接到公园中,求得公园与小区之间的直线距离
    supply_copy['length'] = supply_copy[['x_left','y_left','x_right','y_right']].apply(lambda x:haversine(x[0],x[1],x[2],x[3]),axis=1)
    supply_vk = supply_copy.groupby(by='id_left').apply(get_Rj).reset_index()
    supply_vk.columns=['id','vl_R']
    supply_concat = pd.merge(supply_df,supply_vk,on='id')
    return supply_concat

def step02(supply_concat,demand):
    #第二步计算
    #对住宅区进行缓冲
    demand_copy = demand.copy() 
    demand_copy['geometry'] = demand_copy['geometry'].buffer(1098)
    demand_copy = gpd.sjoin(demand_copy,supply_concat,op='intersects')
    demand_copy['length'] = demand_copy[['x_right', 'y_right','x_left', 'y_left']].apply(lambda x:haversine(x[0],x[1],x[2],x[3]),axis=1)
    demand_vl = demand_copy.groupby(by='id_left').apply(get_A).reset_index()

    demand_vl.columns=['id','vl_R']
    dt = demand.merge(demand_vl,on='id')
    return dt

net = gpd.read_file("/Users/creative/Documents/python/Accessibility/2SFCA/pop_net.geojson")
school = gpd.read_file("/Users/creative/Documents/python/Accessibility/2SFCA/深圳学校.geojson")
hospital = gpd.read_file("/Users/creative/Documents/python/Accessibility/2SFCA/社康面积.geojson")
hospital["id"] = list(range(0,len(hospital))) #添加ID

#转换坐标系 转换为可计算的投影坐标系
school = school.to_crs(epsg=3857)
hospital = hospital.to_crs(epsg=3857)

#dt = step02(step01(school,net),net)
#dt.to_file('/Users/creative/Desktop/学校2SCFA.shp',encoding = 'gb18030') 

dt2 = step02(step01(hospital,net),net)
dt2.to_file('/Users/creative/Desktop/医院2SCFA.shp',encoding = 'gb18030') 