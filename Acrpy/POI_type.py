import pandas as pd
import numpy as np
from IPython.display import display

file_path = 'F:\\我的坚果云\\时空行为数据收集\\POI分类.xlsx'
df_sheet = pd.read_excel(file_path, sheet_name=0, header=0)
A = []
B = []
C = []
A1 = []
A2 = []
A3 = []
B1 = []
B2 = []
B3 = []
B4 = []
C1 = []
C2 = []

for i in range(len(df_sheet)):
    a = df_sheet.loc[i,"Spatial"]
    b = df_sheet.loc[i,"Type"]
    c = df_sheet.loc[i,"Code"]
    if a == "防疫性空间":
        A.append(str(c))
    if a == "疗愈性空间":
        B.append(str(c))
    if a == "保障性空间":
        C.append(str(c))
    
for i in range(len(df_sheet)):
    b = df_sheet.loc[i,"Type"]
    if b=="医疗服务设施":
        A1.append(str(c))
    if b == "避难收容设施":
        A2.append(str(c))
    if b == "临时收容设施":
        A3.append(str(c))
    if b == "自然接触设施":
        B1.append(str(c))
    if b == "需求供给设施":
        B2.append(str(c))
    if b == "灵修陶冶设施":
        B3.append(str(c))
    if b == "体育锻炼设施":
        B4.append(str(c))
    if b == "交通保障设施":
        C1.append(str(c))
    if b == "生活保障设施":
        C2.append(str(c))
    

print ("A = {}".format(A))
print ("B = {}".format(B))
print ("C = {}".format(C))
print ("A1 = {}".format(A1))
print ("A2 = {}".format(A2))
print ("A3 = {}".format(A3))
print ("B1 = {}".format(B1))
print ("B2 = {}".format(B2))
print ("B3 = {}".format(B3))
print ("B4 = {}".format(B4))
print ("C1 = {}".format(C1))
print ("C2 = {}".format(C2))


