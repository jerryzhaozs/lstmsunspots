import jieba

#语料句子
sentence_ori="研究生物很有意思。他大学时代是研究生物的。生物专业是他的首选目标。他是研究生。"
#测试句子
sentence_test=input()
#任务：编写平滑函数完成数据平滑，利用平滑数据完成对2-gram模型的建立，计算测试句子概率并输出结果
# ********** Begin *********#
def gt(N, c):
    if c+1 not in N:
        cx = c+1
    else:
        cx = (c+1) * N[c+1]/N[c]
    return cx
jieba.setLogLevel(jieba.logging.INFO)
sentence_ori = sentence_ori[:-1]
words = jieba.lcut(sentence_ori)
words.insert(0, "BOS")
words.append("EOS")
i = 0
lengh = len(words)
while i < lengh:
    if words[i] == "。":
        words[i] = "BOS"
        words.insert(i, "EOS")
        i += 1
        lengh += 1
    i += 1
phrases = []
for i in range(len(words)-1):
    phrases.append(words[i]+words[i+1])
phrasedict = {}
for phrase in phrases:
    if phrase not in phrasedict:
        phrasedict[phrase] = 1
    else:
        phrasedict[phrase] += 1
words_test = jieba.lcut(sentence_test)
words_test.insert(0, "BOS")
words_test.append("EOS")
phrases_test = []
for i in range(len(words_test)-1):
    phrases_test.append(words_test[i]+words_test[i+1])
pdict = {}
for phrase in phrases_test:
    if phrase not in phrasedict:
        pdict[phrase] = 0
    else:
        pdict[phrase] = phrasedict[phrase]
N = {}
for i in pdict:
    if pdict[i] not in N:
        N[pdict[i]] = 1
    else:
        N[pdict[i]] += 1
N[0] += 1
Nnum = 0
for i in N:
    Nnum += i*N[i]
p = 1
for phrase in phrases_test:
    c = pdict[phrase]
    cx = gt(N, c)
    p *= cx/Nnum
print(p)
 # ********** End **********#
    