import jieba

# 语料句子
sentence_ori = "研究生物很有意思。他大学时代是研究生物的。生物专业是他的首选目标。他是研究生。"

# 测试句子
sentence_test = input()

# 对语料句子进行分词
tokens = jieba.cut(sentence_ori)

# 计算2-gram的概率
t_dict = {}
for sentence in tokens:
    words = sentence.split()
    for i in range(len(words) - 1):
        sentence = words[i] + ' ' + words[i + 1]
        if sentence in t_dict:
            t_dict[sentence] += 1
        else:
            t_dict[sentence] = 1

# 统计每个单词出现的次数，用来计算概率
word_freq = {}
for word in jieba.cut(sentence_ori):
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# 计算测试语句的概率
tokens = jieba.cut(sentence_test)
p = 1
for word in tokens:
    if word in word_freq:
        p *= word_freq[word] / len(word_freq)
    else:
        p *= 0

print(p)
