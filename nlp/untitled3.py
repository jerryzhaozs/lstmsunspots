# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:32:39 2023

@author: ai4agr@126.com
"""
import jieba
from gensim.models import Word2Vec
import re
inputs = open("sg1.txt", 'r', encoding='utf-8')
stopword = [line.strip() for line in open("stopwords-cn.txt", 'r').readlines()]
lines = []
for line in inputs:  # 分别对每段分词
    temp = jieba.lcut(line)  # 分词
    words = []
    for i in temp:
        # 过滤标点符号
        i = re.sub("[\s+.!/_,$“”%^*(\"\'”《》]+|[+—！，。？、~@#￥%…&*（）：；‘-]+|[他，她]", "", i)
        if i not in stopword:
            words.append(i)
    if len(words) > 0:
        lines.append(words)
# 调用Word2Vec训练
model = Word2Vec(lines, vector_size=20, window=2, min_count=3, epochs=7, negative=10, sg=1)
print("刘备的词向量: \n", model.wv.get_vector('刘备'))  # 共计20个数值，表示刘备的词向量
print("和刘备相关性最高的前10个词语: ")  # 与刘备最相关的前10个词语
result = model.wv.most_similar('刘备', topn=10)
for i in result:
    print(i)