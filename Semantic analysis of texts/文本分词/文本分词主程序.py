import sys,codecs
import jieba.posseg
import jieba.analyse
from collections import Counter
import pandas as pd
import re

# 数据清晰，去掉表情与符号
def clean_data(Text):
    a = []
    for i in Text:
        pattern1='[a-zA-Z0-9]'
        pattern2 = '\[.*?\]'
        pattern3 = re.compile(u'[^\s1234567890:：' + '\u4e00-\u9fa5]+')
        pattern4='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
        line1=re.sub(pattern1,'',i)   #去除英文字母和数字
        line2=re.sub(pattern2,'',line1)   #去除表情
        line3=re.sub(pattern3,'',line2)   #去除其它字符
        line4=re.sub(pattern4, '', line3) #去掉残留的冒号及其它符号
        new_sentence=''.join(line4.split())
        if new_sentence != "":
            a.append(new_sentence)
    return a

# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    l = []
    pos = ['n','ns', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l


# 主函数
if __name__ == "__main__":
    # 自定义jieba词库，引入自己制作第情感词典与停用词库
    jieba.load_userdict("semantic_dic.txt") #加入情感词典
    stopkey = [w.strip() for w in codecs.open('stop_word.txt', 'r',encoding='utf-8').readlines()]

    # 数据导入与处理
    Text_dataset = pd.read_excel("comment_neg.xlsx",sheet_name=0,header=0)
    row_num=Text_dataset.shape[0]
    data = []
    number = 0
    for i in range(row_num):
        Text=str(Text_dataset.iloc[i,6])
        c = int(row_num/10)

        # 统计任务进度的模块
        number += 1
        if number/c % 1 == 0:
            print("当前文本处理任务进度{:.0%}".format(number/row_num))
        
        result = dataPrepos(Text,stopkey) # 文本预处理
        result = clean_data(result)
        """遍历，把所有数据都加入到一个list里"""
        for a in result:
            data.append(a)
    test = Counter(data)   #词频统计工具
    k = test.most_common(len(test)) #依据次数排序

    #保存为excel
    collects = []
    for i in k:
        a = {"key":str(i[0]),"count":str(i[1])}
        collects.append(a)
    df = pd.DataFrame(columns=["key","count"])
    df = df.append(collects,ignore_index=True)  
    df.to_excel("neg词频统计表.xlsx")
    print("\n【程序提示】\n任务处理完成，已分割出{}个词".format(len(collects)))