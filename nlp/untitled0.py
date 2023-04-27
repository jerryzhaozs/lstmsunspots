# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:54:19 2023

@author: Ai4agr
"""

import jieba
# 'C:/Users/Administrator/Desktop/lstm/nlp/sg.txt'
# txt=open('C:/Users/Administrator/Desktop/lstm/nlp/sg.txt','r',encoding='ANSI').read()

# seg_str = "好好学习，天天向上。"

# print("/".join(jieba.lcut(seg_str)))    # 精简模式，返回一个列表类型的结果
# print("/".join(jieba.lcut(seg_str, cut_all=True)))      # 全模式，使用 'cut_all=True' 指定 
# print("/".join(jieba.lcut_for_search(seg_str)))     # 搜索引擎模式


def stopwordslist():
    stopwords = [line.strip() for line in open(r'stopwords-cn.txt',encoding='gbk').readlines()]
    return stopwords

def seg_depart(sentence,counts):
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if len(word)>1:
                counts[word]=counts.get(word,0)+1
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
 
# 给出文档路径
filename = r"sg1.txt"
outfilename = r"sg-out.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')
counts={}
# 将输出结果写入out.txt中
lines=[]
for line in inputs:
    line_seg = seg_depart(line,counts)
    outputs.write(line_seg + '\n')
#%%
ls1 = sorted(counts.items(),key=lambda x:x[1],reverse=True)
for i in ls1[:20]:
    print(f'{i[0]}->{i[1]}')
outputs.close()
inputs.close()

#%%

# from gensim.models import Word2Vec
# import re

# inputs = open('sg-out.txt', 'r', encoding='UTF-8')
# lines=[]
# print(inputs)





# model=Word2Vec(inputs,vector_size=20,window=2,min_count=3,epochs=7,negative=10,sg=1)
# print(model.wv.get_vector('刘备'))
# result=model.wv.most_similar('刘备',topn=10)
# for i in result:
#     print(i)
# inputs.close()