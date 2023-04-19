# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:19:10 2023

@author: ai4agr@126.com
"""

import logging
from gensim.models import word2vec

def getmodel():
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

  # 加载《人民的名义》文本
  sentences = word2vec.LineSentence('./sg1.txt')
  
  
# 任务：使用 gensim 模块中的word2vec对sentences文本构建合适的word2vec模型，并保存到model变量中，使得文本中的人名相近度达0.85以上。
# ********** Begin *********#
  model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=3, vector_size=100)
# ********** End **********#
  return model
a=getmodel()
