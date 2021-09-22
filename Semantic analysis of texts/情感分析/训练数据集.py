# coding: utf-8
from snownlp import SnowNLP
from snownlp import sentiment

file_path=r'pos1.txt'   #积极数据集
file_path2=r'neg1.txt'   #消极数据集
sentiment.train(file_path2, file_path) 
sentiment.save(r'sentiment1.marshal')