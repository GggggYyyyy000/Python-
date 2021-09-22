import jieba
import pandas as pd
 
def replaceSynonymWords(words):
    # 1读取同义词表，并生成一个字典。
    combine_dict = {}
    # synonymWords.txt是同义词表，每行是一系列同义词，用空格分割
    for line in open("/Users/creative/Documents/python/Semantic analysis of texts/情感词典/ChineseSemanticKB-master/dict/cilin_ex.txt", "r", encoding='utf-8'):
        seperate_word = line.strip().split(" ")
        del seperate_word[0]
        num = len(seperate_word)
        for i in range(1, num):
            combine_dict[seperate_word[i]] = seperate_word[0]

        if words in combine_dict:
            new_words = combine_dict[words]
        
    return new_words


df = pd.read_excel("手动筛选数据.xlsx",sheet_name=0)

synonyword = []
for i in range(len(df)):
    key = df.loc[i,"key"]
    try:
        synonyword.append(replaceSynonymWords(key))
    except:
        synonyword.append(" ")

df["synonyword"] = synonyword
df.to_excel("synonyword.xlsx")
    
