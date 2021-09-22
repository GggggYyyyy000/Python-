# coding: utf-8
from snownlp import SnowNLP
from snownlp import sentiment
import pandas as pd
from IPython.display import display

file_path=r'pos1.txt'
file_path2=r'neg1.txt'
sentiment.train(file_path2, file_path) 
sentiment.save(r'sentiment1.marshal')

file_path3=r'custom_data.xlsx'
file_path4=r'custom_data_1.xlsx'
df_sheet=pd.read_excel(file_path3,sheet_name=0,header=0)
row_num=df_sheet.shape[0]
col_num=df_sheet.shape[1]
df_sheet['sentiments']=0
df_sheet['forcast']=0
display(df_sheet)
for i in range(row_num):
    text=df_sheet.iloc[i,0]
    s2=SnowNLP(text).sentiments
    df_sheet.iloc[i,2]=s2
    if(s2>=0.6):
        df_sheet.iloc[i,3]=1
    else:
        df_sheet.iloc[i,3]=0
counts=0
for i in range(row_num):
    if(df_sheet.iloc[i,3]==df_sheet.iloc[i,1]):
        counts+=1
print(counts/row_num)
df_sheet.to_excel(file_path4, index=False) 
