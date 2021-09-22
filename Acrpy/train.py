# -*- coding: utf-8 -*-
import json
import math
import arcpy

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def wgs84togcj02(lng, lat):
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02towgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
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
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def main(lng,lat):
    lng = float(lng)
    lat = float(lat)
    #[lng,lat]=[112.917724,28.230401]
    [dstlng, dstlat] = gcj02towgs84(lng, lat)
    a = []
    a.append(dstlng)
    a.append(dstlat)
    return a

if __name__ == '__main__':
    #fc = r"D:\\python\\Acrpy\\data\\Bus_Station_NS.shp"   
    fc = arcpy.GetParameterAsText(0)
    lng = arcpy.GetParameterAsText(1)
    lat = arcpy.GetParameterAsText(2)
    count = arcpy.GetCount_management(fc)
    try:
        arcpy.AddField_management(fc, "lng84", "DOUBLE")     #添加字段
        arcpy.AddField_management(fc, "lat84", "DOUBLE")     #添加字段
        arcpy.AddMessage("新的字段添加成功，分别命名为lng84和lat84")
    except:
        arcpy.AddWarning("字段已存在，添加失败")
    cursor = arcpy.UpdateCursor(fc)                                  #更新游标，此操作的目的是为了更改属性表的属性
    number = 0
    for row in cursor:
        number = number + 1
        arcpy.AddWarning("正在处理第{}个数据，共计{}数据需处理".format(number,count))
        location = main(row.getValue(lng),row.getValue(lat))
        row.setValue("lng84", location[0])                         #更新字段的值
        row.setValue("lat84", location[1])
        cursor.updateRow(row)