import pandas as pd

file_path = "CNKI-20210804145954042.txt"

fp=open(file_path)
lines = fp.readlines()

"""整合成一个文本"""
a = ""
for i in lines:
    a = a+i

data = a.split("%W CNKI") #分割文献
del data[len(data)-1]

cnki = []
for i in data:
    Author = []
    for i in i.split("%"):
        if i[0:1] == "T":
            title = i
        if i[0:1] == "J":
            Journal = i
        if i[0:1] == "D":
            year = i 
        if i[0:1] == "K":
            keywords = i 
        if i[0:1] == "X":
            Abstract = i 
        if i[0:1] == "A": 
            Author.append(i)
    """多作者情况转换为一列"""
    aa = ""
    for a in Author:
        aa = aa + a + ";"
    literature = {"Title":title.replace("T ","").replace("\n",""),
                "Journal":Journal.replace("J ","").replace("\n",""),
                "Year":year.replace("D ","").replace("\n",""),
                "Author":aa.replace("A ","").replace("\n",""),
                "Abstract":Abstract.replace("X ","").replace("\n",""),
                "keywords":keywords.replace("K ","").replace("\n","")}
    cnki.append(literature)

df = pd.DataFrame(columns=["Title","Journal","Year","Author","Abstract","keywords"])
df = df.append(cnki,ignore_index=True)
df.to_excel("/Users/creative/Documents/python/工具箱/文献工具/CNKI.xlsx",encoding="utf_8_sig") 

