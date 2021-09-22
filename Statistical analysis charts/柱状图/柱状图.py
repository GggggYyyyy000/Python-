import matplotlib.pyplot as plt
import pandas as pd

file_path = "D:\python\Statistical analysis charts\柱状图\data.xlsx"
a = pd.read_excel(file_path)
lables = []
park_one = []
park_two = []
park_three = []
width = 0.35  
for i in range(len(a)):
    lables.append(a.loc[i,"区域"])
    park_one.append(a.loc[i,"城市公园"])
    park_two.append(a.loc[i,"社区公园"])
    park_three.append(a.loc[i,"自然公园"])

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#font = "D:\python\Statistical analysis charts\张海山草泥马体.ttf"
plt.bar(lables, park_one, color='#000000', label='城市公园')
plt.bar(lables, park_two, bottom=park_one, color='#f0f0f0', label='社区公园')
plt.bar(lables, park_three, bottom=park_one, color='#dfdfdf', label='自然公园')

plt.ylabel('公园数量',fontsize=12)
plt.xlabel('深圳市行政区',fontsize=12)
# 添加图例
plt.legend(loc='upper right')
plt.savefig('D:\python\Statistical analysis charts\柱状图\深圳公园数量.jpg') 
plt.show()