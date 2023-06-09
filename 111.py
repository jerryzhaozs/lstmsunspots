import pandas as pd
path = 'C:\\Users\\Administrator\\Desktop\\emotion\\'
pd_all = pd.read_csv(path + 'simplifyweibo_4_moods.csv')
moods = {0: '喜悦', 1: '愤怒', 2: '厌恶', 3: '低落'}

print('微博数目（总体）：%d' % pd_all.shape[0])

for label, mood in moods.items(): 
    print('微博数目（{}）：{}'.format(mood,  pd_all[pd_all.label==label].shape[0]))

def stopwordslist():
    stopwords = [line.strip() for line in open(path+'stopwords-cn.txt',encoding='gbk').readlines()]
    return stopwords

import jieba
import numpy as np
import multiprocessing as mp
from tqdm import tqdm