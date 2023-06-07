import pycrfsuite

# 定义特征函数，对输入文本进行特征提取
def extract_features(text):
    features = []
    for i in range(len(text)):
        # 特征1：当前字符
        features.append('char={}'.format(text[i]))
        
        if i > 0:
            # 特征2：前一个字符和当前字符
            features.append('bigram={}/{}'.format(text[i-1], text[i]))
        
        if i < len(text) - 1:
            # 特征3：当前字符和后一个字符
            features.append('bigram={}/{}'.format(text[i], text[i+1]))
    
    return features

# 加载训练数据集
with open('train.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

X_train, y_train = [], []
for line in lines:
    # 将每个句子按空格划分为单词列表，并去掉结尾的换行符
    words = line.strip().split()
    X_train.append([extract_features(word) for word in words])
    y_train.append([label for label in words])

# 创建CRF模型并训练
trainer = pycrfsuite.Trainer(verbose=False)
for xseq, yseq in zip(X_train, y_train):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,
    'c2': 1e-3,
    'max_iterations': 50,
    'feature.possible_transitions': True
})

trainer.train('crf_model')

# 加载测试数据集，并对每个句子进行分词
with open('test.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

X_test = []
for line in lines:
    # 将每个句子按空格划分为单词列表，并去掉结尾的换行符
    words = line.strip().split()
    X_test.append([extract_features(word) for word in words])

# 加载训练好的模型并预测测试数据集的标签
tagger = pycrfsuite.Tagger()
tagger.open('crf_model')

y_pred = []
for xseq in X_test:
    y_pred.append(tagger.tag(xseq))

# 输出分词结果
for i in range(len(lines)):
    print('原始句子：{}'.format(lines[i].strip()))
    print('分词结果：{}\n'.format(' '.join(y_pred[i])))
