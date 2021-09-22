import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = "china_data.xlsx"
a = pd.read_excel(file_path)

lable = []
Existing_confirmed = []
Cumulative_confirmed = []
Newly_confirmed = []
dead = []
cured = []
growth_rate = []
dead_rate = []
cured_rate = []
for i in range(len(a)):
    lable.append(a.loc[i,"ID"])
    Existing_confirmed.append(a.loc[i,"现有确诊"])
    Cumulative_confirmed.append(a.loc[i,"累计确诊"])
    Newly_confirmed.append(a.loc[i,"新增确诊"])
    dead.append(a.loc[i,"死亡病例"])
    cured.append(a.loc[i,"治愈病例"])
    #growth_rate.append("%.2f%%" % (a.loc[i,"增长率"] * 100))
    growth_rate.append(a.loc[i,"增长率"] * 100)
    dead_rate.append(a.loc[i,"死亡率"])
    cured_rate.append(a.loc[i,"治愈率"])

base_data = {"Growth_Rate":growth_rate}
two_data = {"cured_rate":cured_rate,"dead_rate":dead_rate}
People_data1 = {"Existing_confirmed":Existing_confirmed}
People_data2 = {"Cumulative_confirmed":Cumulative_confirmed}
People_data3 = {"Cured":cured}
fig = plt.figure(figsize=(15,6),dpi=300)
#fig, ax = plt.subplots()
ax = fig.add_subplot(1,2,2)
ax.stackplot(lable, base_data.values(),
             labels=base_data.keys(),color="#013a55")
ax.legend(loc='upper left')
ax.set_title("China's new crown epidemic growth, cure, and mortality changes")
ax.set_xlabel('Days of COVID-19 Outbreak')
ax.set_ylabel('Growth_Rate of change')
ax2=ax.twinx()
plt.plot(lable, 
         cured_rate, 
         label = "Cured_Rate",
         linestyle = '-', 
         linewidth = 2, 
         color = '#c0d0e1', 
         markersize = 6,
         markerfacecolor='#bfd0e1',
         markeredgecolor='black') 
plt.plot(lable, 
         dead_rate,         
         label = "Dead_Rate",
         linestyle = '-', 
         linewidth = 2, 
         color = '#eceae8',
         markersize = 6,
         markerfacecolor='#bfd0e1',
         markeredgecolor='black') 
ax2.legend(loc='upper right')
ax2.set_title("China's new crown epidemic growth, cure, and mortality changes")
ax2.set_ylabel('Cure and Mortality Rate of change')

ax3 = fig.add_subplot(1,2,1)
#plt.axvline(x=67,ls="-",c="black", linewidth=67)  
color = ["#013a55",'#eceae8','#c0d0e1']
ax3.stackplot(lable, Cumulative_confirmed,
             labels=People_data2.keys(),color = "#eceae8")
ax3.stackplot(lable, cured,
             labels=People_data3.keys(),color = "#c0d0e1")   
ax3.stackplot(lable, Existing_confirmed,
             labels=People_data1.keys(),color = "#013a55")       
 
ax3.legend(loc='upper right')
ax3.set_title("Trend of diagnosis and cure of new crown patients in China")
ax3.set_xlabel('Days of COVID-19 Outbreak')
ax3.set_ylabel('Number of people')

plt.savefig('中国疫情暴发趋势统计.jpg') 
plt.show()
