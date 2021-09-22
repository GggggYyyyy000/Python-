import jieba
from collections import Counter
import pandas as pd
import re
import logging
import multiprocessing
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# sklean 库
from sklearn.metrics import confusion_matrix,precision_recall_fscore_support

import warnings
warnings.filterwarnings('ignore')

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

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
 
# 对句子进行分词
def seg_sentence(sentence,stopwords): 
    sentence_seged = jieba.cut(sentence.strip())
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    outstr = outstr.split(" ")
    return outstr

# 主函数
if __name__ == "__main__":
    # 自定义jieba词库，引入自己制作第情感词典与停用词库
    jieba.load_userdict("/Users/creative/Documents/python/Semantic analysis of texts/文本分词/semantic_dic.txt") #加入情感词典
    stopwords = stopwordslist('/Users/creative/Documents/python/Semantic analysis of texts/文本分词/stop_word.txt')  # 这里加载停用词的路径

    # 数据导入与处理
    Text_dataset = pd.read_excel("train_data.xlsx",sheet_name=0,header=0)
    row_num=Text_dataset.shape[0]
    data = []
    number = 0
    for i in range(row_num):
        Text=str(Text_dataset.iloc[i,5])
        c = int(row_num/10)

        # 统计任务进度的模块
        number += 1
        if number/c % 1 == 0:
            print("当前文本处理任务进度{:.0%}".format(number/row_num))
        
        result = seg_sentence(Text,stopwords)
        result = clean_data(result)
        """遍历，把所有数据都加入到一个list里"""
        data.append(result)
    print("\n【程序提示】\n任务处理完成，已分割{}数据".format(len(data)))

    #文本向量化模型训练，保存两个训练集
    model = Word2Vec(data, size=200, window=5, min_count=5,workers=multiprocessing.cpu_count())
    model.save('news_word2vec_200.w2v')
    model.wv.save_word2vec_format('news_word2vec_200.bin',binary=False) 
    