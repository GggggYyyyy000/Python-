import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

"""定义图框"""
fig = plt.figure(figsize=(30,18),dpi=300)

"""年龄金字塔图绘制"""
ax1 = fig.add_subplot(2,2,3)
Pyramid_Data = pd.read_excel("data.xlsx")
bar_plot = sns.barplot(y = 'pyramid', x = "Femla", color = "#013a55", data = Pyramid_Data,
                      order = ['95-99','90-94','85-89','80-84',
                               '70-74','75-79','65-69','60-64','55-59',
                               '50-54','45-49','40-44','35-39','30-34',
                               '25-29','20-24','15-19','10-14','5-9','0-4'],
                               label = "Female",)
bar_plot2 = sns.barplot(y = 'pyramid', x = "Male", color = "#bfd0e1", data = Pyramid_Data,
                      order = ['95-99','90-94','85-89','80-84',
                               '70-74','75-79','65-69','60-64','55-59',
                               '50-54','45-49','40-44','35-39','30-34',
                               '25-29','20-24','15-19','10-14','5-9','0-4'],
                               label = "Male",)
plt.title("Number distribution of male patients and female patients",fontsize=25)
plt.xlabel("Number",fontsize=25)
plt.ylabel("Age",fontsize=25)
plt.legend(fontsize = "xx-large")

"""年龄趋势图绘制"""
ax2 = fig.add_subplot(2,2,4)
plt.plot(Pyramid_Data["pyramid"], # x轴数据
         Pyramid_Data["Femla2"], # y轴数据
         label = "Female",
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#eceae8', # 折线颜色
         markersize = 6,
         markerfacecolor='#bfd0e1',
         markeredgecolor='black') # 点的大小
plt.plot(Pyramid_Data["pyramid"], # x轴数据
         Pyramid_Data["Male"], # y轴数据         
         label = "Male",
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#c0d0e1', # 折线颜色
         markersize = 6,
         markerfacecolor='#bfd0e1',
         markeredgecolor='black') # 点的大小
plt.plot(Pyramid_Data["pyramid"], # x轴数据
         Pyramid_Data["sum"], # y轴数据
         label = "Sum",
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#013a55', # 折线颜色
         markersize = 6,
         markerfacecolor='#bfd0e1',
         markeredgecolor='black') # 点的大小
# 添加标题和坐标轴标签
plt.title('Trend chart of overall patient age distribution',fontsize=25)
plt.xlabel('Age',fontsize=25)
plt.ylabel('Number',fontsize=25)
plt.legend(fontsize = "xx-large")

"""箱线图绘制"""
data = "【7k+】患者年龄性别筛选.xlsx"
df = pd.read_excel(data, sheet_name=0, header=0)
gender = df.groupby("judge")      #分组
Male = gender.get_group("男")     #提取组内标签为男的信息
Female = gender.get_group("女")   #提取组内标签为女的信息

ax3 = fig.add_subplot(2,1,1)
plt.boxplot(df["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#003953'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
plt.boxplot(Female["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#eceae8'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
plt.boxplot(Male["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#c0d0e1'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
plt.title('Overall patient age structure',fontsize=25)
plt.ylabel("Age",fontsize=25)
plt.boxplot(Female["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#eceae8'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})

plt.savefig('患者年龄信息图23.jpg') #保存图片
plt.show()