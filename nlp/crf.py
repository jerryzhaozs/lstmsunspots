# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 08:57:53 2023

@author: Administrator
"""

import pycrfsuite
import jieba
import re

# 1. 语料预处理
def preprocess(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            words = jieba.cut(line.strip())
            features = [{'word': word, 'type': 'B'} for word in words]
            data.append(features)
    return data

train_data = preprocess('C:\\Users\\Administrator\\Desktop\\lstm\\nlp\\train.txt')
test_data = preprocess('C:\\Users\\Administrator\\Desktop\\lstm\\nlp\\test.txt')

# 2. 训练模型
def train(train_data, model_path):
    trainer = pycrfsuite.Trainer(verbose=False)
    for features in train_data:
        labels = []
        for word in features:
            labels.append(word['type'])
        trainer.append(features, labels)
    trainer.set_params({
        'c1': 0.1,
        'c2': 0.01,
        'max_iterations': 200,
        'feature.possible_transitions': True
    })
    trainer.train(model_path)

train(train_data, 'model.crfsuite')

# 3. 准备并测试语料
def predict(test_data, model_path):
    tagger = pycrfsuite.Tagger()
    tagger.open(model_path)
    pred_results = []
    for features in test_data:
        labels = tagger.tag(features)
        pred_results.append(labels)
    return pred_results

pred_results = predict(test_data, 'model.crfsuite')

# 4. 将标注的词位信息转化为分词和标注结果
def extract(result):
    extract_results = []
    for i, labels in enumerate(result):
        extract_result = []
        features = test_data[i]
        if len(features) == 0:
            extract_results.append(extract_result)
            continue
        for j, label in enumerate(labels):
            word = features[j]['word']
            if label == 'B':
                extract_result.append(word)
            else:
                extract_result[-1] += word
        extract_results.append(extract_result)
    return extract_results


extract_results = extract(pred_results)

# 5. 评估结果
with open('C:\\Users\\Administrator\\Desktop\\lstm\\nlp\\test_result.txt', 'w', encoding='utf-8') as f:
    for line in extract_results:
        f.write('  '.join(line) + '\n')
        for word in line:
            print(word,end=' ')