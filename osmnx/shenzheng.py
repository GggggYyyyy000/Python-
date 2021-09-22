# coding: utf-8
import pandana, time, os, pandas as pd, numpy as np
from pandana.loaders import osm
import matplotlib.pyplot as plt

# 基础配置区域，包括POI的类型，搜索距离，与城市边界
amenities = ['safeguard']
distance = 1000
num_pois = 10
num_categories = len(amenities) + 1 
bbox = [22.4307, 113.7305, 22.8426, 114.6362] 

# 配置文件名以保存/加载POI和网络数据集
bbox_string = '_'.join([str(x) for x in bbox])
net_filename = 'D:\\python\\osmnx\\Data\\network_{}.h5'.format(bbox_string)
poi_filename = 'D:\\python\\osmnx\\Data\\safeguard.csv'

# matplotlib绘图参数设置
bbox_aspect_ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])
fig_kwargs = {'facecolor':'w', 
              'figsize':(10, 10 * bbox_aspect_ratio)}
plot_kwargs = {'s':2, 
               'alpha':0.9, 
               'cmap':'viridis_r', 
               'edgecolor':'none'}
agg_plot_kwargs = plot_kwargs.copy()
agg_plot_kwargs['cmap'] = 'viridis'
hex_plot_kwargs = {'gridsize':120,
                   'alpha':0.9, 
                   'cmap':'viridis_r', 
                   'edgecolor':'none'}
cbar_kwargs = {}
bmap_kwargs = {}
bgcolor = 'k'

#POI文件导入
if os.path.isfile(poi_filename):
    pois = pd.read_csv(poi_filename)
    method = 'loaded from CSV'
    print ("POI数据导入成功")
else:   
    print ("poi数据不存在")

# OSM数据导入，如果没有就按照bbox范围从API中下载，
if os.path.isfile(net_filename):
    network = pandana.network.Network.from_hdf5(net_filename)
    method = 'loaded from HDF5'
    print ("OSM数据导入成功")
else:
    network = osm.pdna_network_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    method = 'downloaded from OSM'
    lcn = network.low_connectivity_nodes(impedance=1000, count=10, imp_name='distance')
    network.save_hdf5(net_filename, rm_nodes=lcn) 
    print ("OSM数据下载成功")

# 网络结构优化，转换为Axial Network / 其实也可以用Dual Network
network.precompute(distance + 1)
network.init_pois(num_categories=num_categories, max_dist=distance, max_pois=num_pois)
network.set_pois(category='all', x_col=pois['lon'], y_col=pois['lat'])
all_access = network.nearest_pois(distance=distance, category='all', num_pois=num_pois)
all_access.head()

fig = plt.figure(figsize=(30,18),dpi=300)
# 距最近疫情小区的距离，六边形绘图法
bmap, fig, ax = network.plot(all_access[1], bbox=bbox, plot_type='hexbin', plot_kwargs=hex_plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Shenzhen Guaranteed Space Assessment', fontsize=12)
fig.savefig('D:\\python\\osmnx\\images\\Shenzhen Guaranteed Space Assessment-Hexagon.png', dpi=300, bbox_inches='tight')

# 距最近疫情小区的距离，散点绘图法
for amenity in amenities:
    pois_subset = pois[pois['amenity']==amenity]
    network.set_pois(category=amenity, x_col=pois_subset['lon'], y_col=pois_subset['lat'])
Community_access = network.nearest_pois(distance=distance, category='safeguard', num_pois=num_pois)
bmap, fig, ax = network.plot(Community_access[1], bbox=bbox, plot_kwargs=plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Shenzhen Guaranteed Space Assessment', fontsize=12)
fig.savefig('D:\\python\\osmnx\\images\\Shenzhen Guaranteed Space Assessment.png', dpi=300, bbox_inches='tight')