# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt

data = "【7k+】患者年龄性别筛选.xlsx"
df = pd.read_excel(data, sheet_name=0, header=0)
gender = df.groupby("judge")
Male = gender.get_group("男")
Female = gender.get_group("女")

fig = plt.figure(figsize=(10,6),)
ax3 = fig.add_subplot(2,3,1)
plt.boxplot(df["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'pink'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
a = list(df["age"].describe())
plt.axhline(y=df["age"].median(),ls=":",c="black")
plt.axhline(y=a[3],ls=":",c="black")
plt.axhline(y=a[4],ls=":",c="black")
plt.axhline(y=a[6],ls=":",c="black")
plt.axhline(y=a[7],ls=":",c="black")
plt.xlabel('Overall patient age structure')
plt.ylabel("Age")
plt.legend()

ax4 = fig.add_subplot(2,3,2)
plt.boxplot(Male["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'lightblue'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
b = list(Male["age"].describe())
plt.axhline(y=Male["age"].median(),ls=":",c="black")
plt.axhline(y=b[3],ls=":",c="black")
plt.axhline(y=b[4],ls=":",c="black")
plt.axhline(y=b[6],ls=":",c="black")
plt.axhline(y=b[7],ls=":",c="black")
plt.xlabel("Age structure of Male patients")
plt.ylabel("Age")
plt.legend()

ax5 = fig.add_subplot(2,3,3)
plt.boxplot(Female["age"],sym="o",patch_artist=True,medianprops={'linestyle':'--','color':'black'},boxprops={'color':'black','facecolor':'lightgreen'}, whiskerprops = {'color': "black"},capprops = {'color': "black"},flierprops={'color':'purple','markeredgecolor':"purple"})
c = list(Female["age"].describe())
plt.axhline(y=Female["age"].median(),ls=":",c="black")
plt.axhline(y=c[3],ls=":",c="black")
plt.axhline(y=c[4],ls=":",c="black")
plt.axhline(y=c[6],ls=":",c="black")
plt.axhline(y=c[7],ls=":",c="black")
plt.xlabel("Age structure of Female patients")
plt.ylabel("Age")
plt.legend()

plt.show()