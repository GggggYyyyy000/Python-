import geo_boundary as gb
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString,Point,Polygon,mapping

def point_to_line(df,num):
    from shapely.geometry import LineString,Point
    dataGroup = df.groupby(num) #分组
    #构造数据
    tb = []
    geomList = []
    for name,group in dataGroup:
        # 分离出属性信息，取每组的第1行前5列作为数据属性
        tb.append(group.iloc[0,:6])
        # 把同一组的点打包到一个list中
        xyList = [xy for xy in zip(group.x, group.y)]

        line = LineString(xyList)
        geomList.append(line)

    # 点转线
    geoDataFrame = gpd.GeoDataFrame(tb, geometry = geomList)
    return geoDataFrame

df = pd.read_excel("/Users/creative/Documents/python/工具箱/小区数据下载/乌鲁木齐医院.xlsx")
uid_list = df["uid"].values.tolist()

boundary = gb.main(uid_list)
bl = point_to_line(boundary,"uid")
bl.crs = 'EPSG:4326'
bl = bl.merge(df, on='uid')
bl = bl.drop_duplicates('uid')
bl.to_file('/Users/creative/Desktop/CP1.shp',encoding = 'gb18030') 
