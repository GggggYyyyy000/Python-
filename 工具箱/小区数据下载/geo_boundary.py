import pandas as pd
import os
import uuid
import math
import requests,json,math
from tqdm import tqdm
from requests.adapters import HTTPAdapter

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)

def get_boundary_by_uid(uid):
    bmap_key = 'IXCaOvm2UfSBB32K8miYTVZZveZ8o2yb'
    bmap_boundary_url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&uid=' + uid + '&c=340&ext_ver=new&tn=B_NORMAL_MAP&nn=0&auth=fw9wVDQUyKS7%3DQ5eWeb5A21KZOG0NadNuxHNBxBBLBHtxjhNwzWWvy1uVt1GgvPUDZYOYIZuEt2gz4yYxGccZcuVtPWv3GuxNt%3DkVJ0IUvhgMZSguxzBEHLNRTVtlEeLZNz1%40Db17dDFC8zv7u%40ZPuxtfvSulnDjnCENTHEHH%40NXBvzXX3M%40J2mmiJ4Y&ie=utf-8&l=19&b=(12679382.095,2565580.38;12679884.095,2565907.38)&t=1573133634785'
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    data = s.get(url=bmap_boundary_url, timeout=5, headers={"Connection": "close"})
    data = data.text
    data = json.loads(data)
    try:
        content = data['content']
        if not 'geo' in content:
            return None
        geo = content['geo']
        i = 0
        strsss = ''
        for jj in str(geo).split('|')[2].split('-')[1].split(','):
            jj = str(jj).strip(';')
            if i % 2 == 0:
                strsss = strsss + str(jj) + ','
            else:
                strsss = strsss + str(jj) + ';'
            i = i + 1
        return strsss.strip(";")
    except:
        pass

def transform_coordinate_batch(coordinates):
    bmap_key = 'zfetLGY71RsWuZP3xZKc7WrM0rurWPVd'
    cooed_count = math.ceil(len(coordinates) / 100)
    coords = ''
    for i in range(cooed_count):
        one_coords = coordinates.split(";")[i * 100: i * 100 + 100]
        one_coords_str = ''
        for point in one_coords:
            one_coords_str = one_coords_str + point + ";"
        one_coords_str = one_coords_str.strip(";")
        req_url = 'http://api.map.baidu.com/geoconv/v1/?coords='+one_coords_str+'&from=6&to=5&ak=' + bmap_key
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        data = s.get(req_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
        data = data.text
        try:
            data = json.loads(data)
        except Exception as e:
            print('发送异常，当前坐标：', coordinates)
            return ' '

        if data['status'] == 0:
            result = data['result']
            if len(result) > 0:
                for res in result:
                    lng = res['x']
                    lat = res['y']
                    coords = coords + ";" + str(lng) + "," + str(lat)
    return coords.strip(";")

def main(data_list):
    bmap_key = 'zfetLGY71RsWuZP3xZKc7WrM0rurWPVd'
    csv_file = pd.DataFrame({'uid':data_list})
    a_col = []
    data_csv = {}

    uids,  boundarys = [], []
    for i in tqdm(range(len(csv_file))):
        uid = csv_file['uid'][i]
        uids.append(uid)
        coordinates = get_boundary_by_uid(uid)
        if coordinates is not None:
            coords = transform_coordinate_batch(coordinates)
            boundarys.append(coords)
        else:
            boundarys.append(' ')

    data_csv['uid'] = uids
    data_csv['boundary'] = boundarys
    df = pd.DataFrame(data_csv)


    # 将数据处理为ARCGIS能展示多边形的数据格式
    csv_file = df

    a_col = []
    data_csv = {}
    numbers, xs, ys, uids = [], [], [], []
    index = 1
    for i in range(len(csv_file)):
        boundary = str(csv_file['boundary'][i])
        uid = str(csv_file['uid'][i])
        if boundary != ' ' and boundary != 'nan' and boundary != None:
            for point in boundary.split(";"):
                lng = point.split(",")[0]
                lat = point.split(",")[1]
                #转换为WGS84坐标系
                coord_wgs84 = bd09_to_wgs84(float(lng), float(lat))
                lng = coord_wgs84[0]
                lat = coord_wgs84[1]
                xs.append(lng)
                ys.append(lat)
                numbers.append(index)
                uids.append(uid)
                index = index + 1
    data_csv['number'] = numbers
    data_csv['x'] = xs
    data_csv['y'] = ys
    data_csv['uid'] = uids

    df = pd.DataFrame(data_csv)
    return df
