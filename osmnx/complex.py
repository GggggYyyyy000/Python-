# coding: utf-8
import pandana, time, os, pandas as pd, numpy as np
from pandana.loaders import osm

# 在1公里的最大距离处配置搜索，以获取最多10个最近的兴趣点
amenities = ['restaurant', 'bar', 'school']
distance = 1000
num_pois = 10
num_categories = len(amenities) + 1 #每个设施一个，另加一个额外的设施

# 边界框作为llcrnrlat，llcrnrlng，urcrnrlat，urcrnrlng的列表
bbox = [37.76, -122.35, 37.9, -122.17] #伯克利/奥克兰的纬度/经度边界框

# 配置文件名以保存/加载POI和网络数据集
bbox_string = '_'.join([str(x) for x in bbox])
net_filename = 'D:\\python\\urban-data-science-master\\20-Accessibility-Walkability\\data\\network_{}.h5'.format(bbox_string)
poi_filename = 'D:\\python\\urban-data-science-master\\20-Accessibility-Walkability\\data\\pois_{}_{}.csv'.format('_'.join(amenities), bbox_string)

# 为matplotlib图传递的关键字参数
bbox_aspect_ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])
fig_kwargs = {'facecolor':'w', 
              'figsize':(10, 10 * bbox_aspect_ratio)}

# 传递散点图的关键字参数
plot_kwargs = {'s':5, 
               'alpha':0.9, 
               'cmap':'viridis_r', 
               'edgecolor':'none'}

# 网络聚合图与常规散点图相同，但没有反向的色图
agg_plot_kwargs = plot_kwargs.copy()
agg_plot_kwargs['cmap'] = 'viridis'

# 传递给十六进制bin图的关键字参数
hex_plot_kwargs = {'gridsize':60,
                   'alpha':0.9, 
                   'cmap':'viridis_r', 
                   'edgecolor':'none'}

# 传递参数以制作颜色条的关键字
cbar_kwargs = {}

# 关键字参数传递给底图
bmap_kwargs = {}

# 颜色使轴的背景
bgcolor = 'k'

start_time = time.time()
if os.path.isfile(poi_filename):
    # 如果已经存在兴趣点文件，则只需从中加载数据集
    pois = pd.read_csv(poi_filename)
    method = 'loaded from CSV'
else:   
    # 否则，请在OSM API的边界框中查询指定的便利设施
    osm_tags = '"amenity"~"{}"'.format('|'.join(amenities))
    pois = osm.node_query(bbox[0], bbox[1], bbox[2], bbox[3], tags=osm_tags)
    
    # 使用“ amenity”〜“ school”返回幼儿园等，因此删除所有不只是“ school”的内容，然后保存为CSV
    pois = pois[pois['amenity'].isin(amenities)]
    pois.to_csv(poi_filename, index=False, encoding='utf-8')
    method = 'downloaded from OSM'
    
print('{:,} POIs {} in {:,.2f} seconds'.format(len(pois), method, time.time()-start_time))
pois[['amenity', 'name', 'lat', 'lon']].head()

# 我们检索了每种便利设施的多少个兴趣点？
pois['amenity'].value_counts()

start_time = time.time()
if os.path.isfile(net_filename):
    # 如果街道网络文件已经存在，只需从中加载数据集
    network = pandana.network.Network.from_hdf5(net_filename)
    method = 'loaded from HDF5'
else:
    # 否则，请在指定的边界框中查询OSM API的街道网络
    network = osm.pdna_network_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    method = 'downloaded from OSM'
    
    # 识别连接到给定距离内少于其他节点的某个阈值的节点
    lcn = network.low_connectivity_nodes(impedance=1000, count=10, imp_name='distance')
    network.save_hdf5(net_filename, rm_nodes=lcn) #remove low-connectivity nodes and save to h5
    
print('Network with {:,} nodes {} in {:,.2f} secs'.format(len(network.node_ids), method, time.time()-start_time))

# 预计算范围查询（在此最大距离内的可达节点）
# 因此，只要您使用较小的距离，就会使用缓存的结果
network.precompute(distance + 1)

# 初始化基础的C ++兴趣点引擎
network.init_pois(num_categories=num_categories, max_dist=distance, max_pois=num_pois)

# 使用lon和lat列指定的位置初始化所有便利设施的类别
network.set_pois(category='all', x_col=pois['lon'], y_col=pois['lat'])

# 搜索到网络中每个节点的n个（所有类型的）最近的便利设施
all_access = network.nearest_pois(distance=distance, category='all', num_pois=num_pois)

# 它返回的df的列数等于请求的POI数
# 每个单元代表从节点到n个POI中每个的网络距离
print('{:,} nodes'.format(len(all_access)))
all_access.head()

# 距任何类型的最近设施的距离
n = 1
bmap, fig, ax = network.plot(all_access[n], bbox=bbox, plot_kwargs=plot_kwargs, fig_kwargs=fig_kwargs, 
                             bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to nearest amenity around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-all-east-bay.png', dpi=200, bbox_inches='tight')

# 距任何类型的第五便利设施的距离
n = 5
bmap, fig, ax = network.plot(all_access[n], bbox=bbox, plot_kwargs=plot_kwargs, fig_kwargs=fig_kwargs, 
                             bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to 5th nearest amenity around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-all-5th-east-bay.png', dpi=200, bbox_inches='tight')

# 距任何类型的最近设施的距离，例如六边形
bmap, fig, ax = network.plot(all_access[1], bbox=bbox, plot_type='hexbin', plot_kwargs=hex_plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to nearest amenity around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-all-hexbin-east-bay.png', dpi=200, bbox_inches='tight')

"""5.针对每种便利设施类型分别计算和绘制可访问性,在开始区域指定的便利设施类型：餐馆，酒吧和学校"""
# 使用lon和lat列指定的位置初始化每个便利设施类别
for amenity in amenities:
    pois_subset = pois[pois['amenity']==amenity]
    network.set_pois(category=amenity, x_col=pois_subset['lon'], y_col=pois_subset['lat'])

# 到最近的餐厅的距离
restaurant_access = network.nearest_pois(distance=distance, category='restaurant', num_pois=num_pois)
bmap, fig, ax = network.plot(restaurant_access[1], bbox=bbox, plot_kwargs=plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to nearest restaurant around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-restaurant-east-bay.png', dpi=200, bbox_inches='tight')

# 到最近的酒吧的距离
bar_access = network.nearest_pois(distance=distance, category='bar', num_pois=num_pois)
bmap, fig, ax = network.plot(bar_access[1], bbox=bbox, plot_kwargs=plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to nearest bar around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-bar-east-bay.png', dpi=200, bbox_inches='tight')

# 到最近的学校的距离
school_access = network.nearest_pois(distance=distance, category='school', num_pois=num_pois)
bmap, fig, ax = network.plot(school_access[1], bbox=bbox, plot_kwargs=plot_kwargs, 
                             fig_kwargs=fig_kwargs, bmap_kwargs=bmap_kwargs, cbar_kwargs=cbar_kwargs)
ax.set_axis_bgcolor(bgcolor)
ax.set_title('Walking distance (m) to nearest school around Berkeley/Oakland', fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-school-east-bay.png', dpi=200, bbox_inches='tight')