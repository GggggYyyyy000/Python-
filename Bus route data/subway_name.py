import pandas as pd

df = pd.read_excel("/Users/creative/Documents/python/Bus route data/dtt.xlsx")
city = "南京"
citys = df[df["字段1"] == city]

citybus_name = []
for i in range(len(citys)):
    citybus_name.append({"city":city,"name":citys.loc[i,"字段2"]})

print(citybus_name)

