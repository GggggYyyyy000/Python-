import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = "D:\python\Statistical analysis charts\统计图\数据.xlsx"
a = pd.read_excel(file_path)
font = "D:\python\Statistical analysis charts\统计图\simsun.ttc"
ur = []
industry = []
year = []
for i in range(len(a)):
    ur.append(a.loc[i,"城市更新"])
    industry.append(a.loc[i,"工业区改造"])
    year.append(a.loc[i,"年份"])

People_data1 = {"城市更新":ur}
People_data2 = {"工业区改造":industry}

fig = plt.figure(figsize=(11,4),dpi=300)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
ax = fig.add_subplot(1,1,1)
ax.stackplot(year, industry,
             labels=People_data2.keys(),color = "#c0d0e1")  
ax.set_ylabel('旧工业区相关论文数量',fontsize=12)
ax.set_xlabel('研究年份',fontsize=12)
ax.legend(loc=2)

ax2=ax.twinx()
plt.stackplot(year, ur,
             labels=People_data1.keys(),color = "#eceae8",alpha=0.6)
ax2.legend(loc=1)
ax2.set_ylabel('城市更新相关论文数量',fontsize=12)
  
plt.savefig('D:\python\Statistical analysis charts\统计图\论文数量.jpg') 
plt.show()