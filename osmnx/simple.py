# coding: utf-8
import pandana, matplotlib.pyplot as plt
from pandana.loaders import osm

bbox = [22.4431, 113.8541, 22.6124, 113.9780] 
amenity = 'restaurant'  
distance = 2000  #最大距离（以米为单位）

"""从OpenStreetMap下载兴趣点（POI）和网络数据"""
pois = osm.node_query(bbox[0], bbox[1], bbox[2], bbox[3], tags='"amenity"="{}"'.format(amenity))
pois[['amenity', 'name', 'lat', 'lon']].tail()
network = osm.pdna_network_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3]) 

"""处理网络数据，然后计算可访问性"""
lcn = network.low_connectivity_nodes(impedance=1000, count=10, imp_name='distance')
network.precompute(distance + 1)
network.init_pois(num_categories=1, max_dist=distance, max_pois=7)
network.set_pois(category='my_amenity', x_col=pois['lon'], y_col=pois['lat'])
access = network.nearest_pois(distance=distance, category='my_amenity', num_pois=7)
access.head()

"""绘制可访问性"""
bbox_aspect_ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])
fig_kwargs = {'facecolor':'w', 
              'figsize':(10, 10 * bbox_aspect_ratio)}
plot_kwargs = {'s':5, 
               'alpha':0.9, 
               'cmap':'viridis_r', 
               'edgecolor':'none'}             
n = 1
bmap, fig, ax = network.plot(access[n], bbox=bbox, plot_kwargs=plot_kwargs, fig_kwargs=fig_kwargs) #要安装basemap库
ax.set_axis_bgcolor('k')  #要使用matplotlib 1.5.3
ax.set_title('Walking distance (m) to nearest {} around Nanshang'.format(amenity), fontsize=15)
fig.savefig('D:\\python\\osmnx\\images\\accessibility-community.png', dpi=300, bbox_inches='tight')
plt.show()