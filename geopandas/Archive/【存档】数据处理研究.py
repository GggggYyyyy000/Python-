# # 数据处理研究
# 本文件主要记录如何将数据进行分组、提取、统计、赋值等操作<br />
# 以及空间绘图研究
# %% [markdown]
# ## 1 数据与库导入

# %%
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt


# %%
file_path = "/Users/creative/OneDrive - stu.hit.edu.cn/课程资料/2020 毕业论文/Arcgis_Analysis/Data/Shp/南山街道边界.shp"
anju_path = "/Users/creative/NutstoreCloudBridge/我的坚果云/文件转存区/Win/data/anju_all_data/【投影】2016-2020安居房位置汇总.shp"


# %%
"""删除多余没必要的数据"""
nanshang = gpd.read_file(file_path).to_crs("EPSG:3857")
anju = gpd.read_file(anju_path)
nanshang = nanshang[(nanshang.QSDWMC!="伶仃岛")]
nanshang = nanshang[(nanshang.QSDWMC!="大铲岛")]
nanshang = nanshang[(nanshang.QSDWMC!="小铲岛")]


# %%
"""将数据按年份分组"""
listType = anju['年份'].unique()
data2017 =  anju[anju['年份'].isin([listType[0]])]
data2016 =  anju[anju['年份'].isin([listType[1]])]
data2020 =  anju[anju['年份'].isin([listType[2]])]
data2019 =  anju[anju['年份'].isin([listType[3]])]
data2018 =  anju[anju['年份'].isin([listType[4]])]

# %% [markdown]
# ## 2 统计每类数据的个数以及其他列之和
# 这里用到了geopandas里的属性联接功能<br />
# `country_shapes = country_shapes.merge(country_names, on='iso_a3')`<br />
# https://geopandas.org/mergingdata.html

# %%
"""计数"""
data2016["备注（筹集"].value_counts()


# %%
def count(data):
    import pandas as pd
    count = data["备注（筹集"].value_counts().reset_index() #将计数后的Series转成DataFrame格式
    count = count.rename(columns={'备注（筹集':'type_count',"index":"备注（筹集"})  #修改DataFrame列名称
    data = data.merge(count, on='备注（筹集') #按属性（列名称）匹配
    T1 = 0 
    T2 = 0 
    T3 = 0 
    for i in range(len(data)):
        name = data.loc[i,"备注（筹集"]
        T = data.loc[i,"套数"]
        if name == "竣工" :
            T1 = T + T1
        if name == "基本建成":
            T2 = T + T2
        if name == "筹集项目":
            T3 = T + T3
    df = pd.DataFrame(columns=["备注（筹集","各类型套数"]) 
    df_data = [{"备注（筹集":"竣工","各类型套数":T1},{"备注（筹集":"基本建成","各类型套数":T2},{"备注（筹集":"筹集项目","各类型套数":T3}]
    for i in df_data:
        df = df.append(i,ignore_index=True)
    data = data.merge(df, on='备注（筹集')  
    return data


# %%
data2016 = count(data2016)

# %% [markdown]
# ## 3 绘制柱状图

# %%
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体：解决plot不能显示中文问题
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# %%
fig = plt.figure(figsize=(8,5),dpi=300)
ax = fig.add_subplot(1,2,1)
plt.bar(data2016["备注（筹集"],data2016["type_count"],color="#c0d0e1")
for a,b in zip(data2016["备注（筹集"],data2016["type_count"]): 
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom') 
plt.ylabel("各类型安居房个数（个）",fontsize=5)

ax = fig.add_subplot(1,2,2)
plt.bar(data2016["备注（筹集"],data2016["各类型套数"],color="#013a55")
for a,b in zip(data2016["备注（筹集"],data2016["各类型套数"]): 
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom') 
plt.ylabel("各类型安居房总套数（套）",fontsize=5)

# %% [markdown]
# ## 4 绘制空间分布图

# %%
fig = plt.figure(figsize=(30,10),dpi=300)
#2016
ax = fig.add_subplot(1,5,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2016.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2016.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2016年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)


#2017
ax = fig.add_subplot(1,5,2)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2017.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2017.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2017年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

#2018
ax = fig.add_subplot(1,5,3)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2018.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2018.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2018年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

#2019
ax = fig.add_subplot(1,5,4)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2019.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3)
data2019.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2019年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

#2020
ax = fig.add_subplot(1,5,5)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2020.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2020.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2020年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

plt.savefig('2016-2020安居房空间位置分布图.jpg') 

# %% [markdown]
# ## 5 绘制组合图

# %%
import matplotlib


# %%
fig = plt.figure(figsize=(15,10),dpi=300)
#data2016 = count(data2016)
ax = fig.add_subplot(1,2,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2016.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2016.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2016年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

ax = fig.add_subplot(2,2,2)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2016["备注（筹集"],data2016["type_count"],color="#6891af",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2016["备注（筹集"],data2016["type_count"]): 
    plt.text(a, b-0.6, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房个数（个）",fontsize=12)

ax = fig.add_subplot(2,2,4)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2016["备注（筹集"],data2016["各类型套数"],color="#afc3d1",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2016["备注（筹集"],data2016["各类型套数"]): 
    plt.text(a, b-500, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房总套数（套）",fontsize=12)

plt.savefig('2016年南山区安居房空间位置分布.jpg') 


# %%
data2017 = count(data2017)


# %%
fig = plt.figure(figsize=(15,10),dpi=300)
ax = fig.add_subplot(1,2,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2017.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2017.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2017年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

ax = fig.add_subplot(2,2,2)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2017["备注（筹集"],data2017["type_count"],color="#6891af",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2017["备注（筹集"],data2017["type_count"]): 
    plt.text(a, b-1, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房个数（个）",fontsize=12)

ax = fig.add_subplot(2,2,4)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2017["备注（筹集"],data2017["各类型套数"],color="#afc3d1",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2017["备注（筹集"],data2017["各类型套数"]): 
    plt.text(a, b-1000, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房总套数（套）",fontsize=12)

plt.savefig('2017年南山区安居房空间位置分布.jpg') 


# %%
data2018 = count(data2018)


# %%
fig = plt.figure(figsize=(15,10),dpi=300)
ax = fig.add_subplot(1,2,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2018.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2018.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2018年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

ax = fig.add_subplot(2,2,2)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2018["备注（筹集"],data2018["type_count"],color="#6891af",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2018["备注（筹集"],data2018["type_count"]): 
    plt.text(a, b-1, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房个数（个）",fontsize=12)

ax = fig.add_subplot(2,2,4)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2018["备注（筹集"],data2018["各类型套数"],color="#afc3d1",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2018["备注（筹集"],data2018["各类型套数"]): 
    plt.text(a, b-1000, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房总套数（套）",fontsize=12)

plt.savefig('2018年南山区安居房空间位置分布.jpg') 


# %%
data2019 = count(data2019)


# %%
fig = plt.figure(figsize=(15,10),dpi=300)
ax = fig.add_subplot(1,2,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2019.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2019.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2019年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

ax = fig.add_subplot(2,2,2)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2019["备注（筹集"],data2019["type_count"],color="#6891af",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2019["备注（筹集"],data2019["type_count"]): 
    plt.text(a, b-1, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房个数（个）",fontsize=12)

ax = fig.add_subplot(2,2,4)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2019["备注（筹集"],data2019["各类型套数"],color="#afc3d1",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2019["备注（筹集"],data2019["各类型套数"]): 
    plt.text(a, b-700, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房总套数（套）",fontsize=12)

plt.savefig('2019年南山区安居房空间位置分布.jpg') 


# %%
data2020 = count(data2020)


# %%
fig = plt.figure(figsize=(15,10),dpi=300)
ax = fig.add_subplot(1,2,1)
nanshang.plot(ax=ax, alpha=0.3, edgecolor='k', facecolor='grey', zorder=1)
nanshang.boundary.plot(ax=ax, edgecolor='k',linestyle='-.',linewidth=1, alpha=0.5, zorder=2)
data2020.representative_point().plot(ax=ax,facecolor='white',linewidth=0.1, zorder=3, alpha=0.8)
data2020.plot(column='备注（筹集', cmap='Paired', ax=ax, legend=True,legend_kwds={'loc': 4,"title":"图例","shadow":True}, zorder=4)
ctx.add_basemap(ax, source='http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',zoom=12)
plt.title("2020年南山区安居房空间位置分布",fontsize=12)
plt.xlabel("lng（Pseudo-Mercator）",fontsize=12)
plt.ylabel("lat（Pseudo-Mercator）",fontsize=12)

ax = fig.add_subplot(2,2,2)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2020["备注（筹集"],data2020["type_count"],color="#6891af",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2020["备注（筹集"],data2020["type_count"]): 
    plt.text(a, b-0.3, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房个数（个）",fontsize=12)

ax = fig.add_subplot(2,2,4)
plt.grid(True, linestyle='--', color='grey', alpha=.25)
plt.bar(data2020["备注（筹集"],data2020["各类型套数"],color="#afc3d1",width=0.4,linewidth=1,edgecolor="k")
for a,b in zip(data2020["备注（筹集"],data2020["各类型套数"]): 
    plt.text(a, b-100, '%.0f' % b, ha='center', va= 'bottom',color='white', weight='bold') 
plt.ylabel("各类型安居房总套数（套）",fontsize=12)

plt.savefig('2020年南山区安居房空间位置分布.jpg') 


# %%



