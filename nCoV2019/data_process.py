import pandas as pd
import os
import numpy as np
import pprint

file_path = "D:\\python\\nCoV2019\\Number"
df = pd.DataFrame(columns=["date","country","countryCode","province",'provinceCode','city',"cityCode","confirmed","suspected","cured","dead"])
file_name = []
for i in os.walk(file_path):
    file_name.append(i)
file_name = file_name[0][2]
for i in file_name:
    path = file_path + "\\" + i
    a = pd.read_csv(path)
    for i in range(len(a)):
        city = a.loc[i,"city"]
        province = a.loc[i,"province"]
        if province == "广东省":
            if city is np.nan:
                b = a.loc[i,:]
                print (b)
                df = df.append(b,ignore_index=True)
            else:
                pass
        else:
            pass

df.to_excel("GuangDon_data.xlsx")

										

