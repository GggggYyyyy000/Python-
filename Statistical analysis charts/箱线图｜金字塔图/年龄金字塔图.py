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

People_data1 = {"Sum":Pyramid_Data["sum"]}
People_data2 = {"Male":Pyramid_Data["Male"]}
People_data3 = {"Female":Pyramid_Data["Femla2"]}
ax3 = fig.add_subplot(2,2,4)
ax3.stackplot(Pyramid_Data["pyramid"], Pyramid_Data["sum"],
             labels=People_data1.keys(),
             color = "#eceae8") 
ax3.stackplot(Pyramid_Data["pyramid"], Pyramid_Data["Male"],
             labels=People_data2.keys(),
             color = "#c0d0e1")
ax3.stackplot(Pyramid_Data["pyramid"], Pyramid_Data["Femla2"], 
             labels=People_data3.keys(),
             color = "#013a55")         
ax3.legend(loc='upper right')
ax3.set_title('Trend chart of overall patient age distribution',fontsize=25)
ax3.set_xlabel('Age',fontsize=25)
ax3.set_ylabel('Number',fontsize=25)
plt.legend(fontsize = "xx-large")

"""箱线图绘制"""
data = "【7k+】患者年龄性别筛选.xlsx"
df = pd.read_excel(data, sheet_name=0, header=0)
gender = df.groupby("judge")      #分组
Male = gender.get_group("男")     #提取组内标签为男的信息
Female = gender.get_group("女")   #提取组内标签为女的信息

ax3 = fig.add_subplot(2,3,1)
plt.boxplot(df["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#003953'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
"""下面是添加辅助线的过程"""
a = list(df["age"].describe())
plt.axhline(y=df["age"].median(),ls=":",c="black")
plt.axhline(y=a[3],ls=":",c="black")
plt.axhline(y=a[4],ls=":",c="black")
plt.axhline(y=a[6],ls=":",c="black")
plt.axhline(y=a[7],ls=":",c="black")
plt.title('Overall patient age structure',fontsize=25)
plt.ylabel("Age",fontsize=25)

ax4 = fig.add_subplot(2,3,2)
plt.boxplot(Male["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#c0d0e1'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
b = list(Male["age"].describe())
plt.axhline(y=Male["age"].median(),ls=":",c="black")
plt.axhline(y=b[3],ls=":",c="black")
plt.axhline(y=b[4],ls=":",c="black")
plt.axhline(y=b[6],ls=":",c="black")
plt.axhline(y=b[7],ls=":",c="black")
plt.title("Age structure of Male patients",fontsize=25)
plt.ylabel("Age",fontsize=25)

ax5 = fig.add_subplot(2,3,3)
plt.boxplot(Female["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'#eceae8'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
c = list(Female["age"].describe())
plt.axhline(y=Female["age"].median(),ls=":",c="black")
plt.axhline(y=c[3],ls=":",c="black")
plt.axhline(y=c[4],ls=":",c="black")
plt.axhline(y=c[6],ls=":",c="black")
plt.axhline(y=c[7],ls=":",c="black")
plt.title("Age structure of Female patients",fontsize=25)
plt.ylabel("Age",fontsize=25)

plt.savefig('患者年龄信息图.jpg') #保存图片
plt.show()