import pandas as pd
import os
from tqdm import tqdm
from pandas.core.frame import DataFrame


"""
plate = []
for filename in tqdm(os.listdir("H:\\数据库\\data_out_41\\test")):
    name = "H:\\数据库\\data_out_41\\test\\" + filename
    print(name)
    df = pd.read_csv(name)
    p = df["车牌"].unique()
    for i in p:
        plate.append(i)

data = {"plate":plate}
datas= DataFrame(data)

p2 = datas["plate"].unique()
data2 = {"plate":p2}
da = DataFrame(data2)
print(da)
print(len(da))

#da.to_csv("D:\\python\\工具箱\\货车路径规划\\车牌.csv",encoding="utf_8_sig")
"""
"""
plate = []
for filename in tqdm(os.listdir("H:\\原始数据")):
    name = "H:\\原始数据\\" + filename
    print(name)
    df = pd.read_csv(name)
    p = df.drop_duplicates(subset=['车牌'],keep='first')
    plate.append(p)

datas = pd.concat(plate)
datas = datas.drop_duplicates(subset=['车牌'],keep='first')
datas = datas.reset_index()

print(datas)
print(len(datas))
"""

plate = []
for filename in tqdm(os.listdir("H:\\原始数据")):
    name = "H:\\原始数据\\" + filename
    print(name)
    df = pd.read_csv(name)
    plate.append(df)

datas = pd.concat(plate)
datas = datas.drop_duplicates(subset=['车牌'],keep='first')
datas = datas.reset_index()

print(datas)
print(len(datas))