#!/usr/bin/env python

# coding: utf-8
from snownlp import SnowNLP
import pandas as pd
from IPython.display import display

df_data=pd.DataFrame(columns=['text', 'sentiment'])
file_path='data.txt'
file_path2='data_1.xlsx'

source=open(file_path,"r",encoding='utf-8')
line=source.readlines()
line_num=len(line)

print(line_num)
for i in range(line_num):
    s1=line[i]
    s2=SnowNLP(s1).sentiments
    df_data=df_data.append({'text':s1, 'sentiment':s2},ignore_index=True)
display(df_data)

df_data.to_excel(file_path2, index=False) 