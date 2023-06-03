# 正向最大匹配法
def cutA(sentence, dictA):
    # sentence：要分词的句子
    result = []
    sentenceLen = len(sentence)
    n = 0
    maxDictA = max([len(word) for word in dictA])
    while n < sentenceLen:
        matched = False  # 标记是否匹配到一个词
        for i in range(maxDictA, 0, -1):  # i表示从左向右截取的字符数
            if n + i <= sentenceLen:
                if sentence[n:n+i] in dictA:
                    result.append(sentence[n:n+i])
                    n += i  # 移动指针
                    matched = True
                    break 
        if not matched:  # 如果没有匹配到词，则按一个字符分隔
            result.append(sentence[n])
            n += 1
    # ********** End **********#
    print(result)  # 输出分词结果
    
# 逆向最大匹配法
def cutB(sentence, dictB):
    # sentence：要分词的句子
    result = []
    sentenceLen = len(sentence)
    maxDictB = max([len(word) for word in dictB])
    n = sentenceLen  # 逆向分词，初始时指针指向句子末尾
    while n > 0:
        matched = False
        for i in range(maxDictB, 0, -1):
            if n - i >= 0: 
                if sentence[n-i:n] in dictB:
                    result.append(sentence[n-i:n])
                    n -= i
                    matched = True
                    break
        if not matched:
            result.append(sentence[n-1])
            n -= 1
    print(result[::-1], end="")  # 逆序输出分词结果
    
# 双向最大匹配算法
class BiMM():
    def __init__(self):
        self.window_size = 3  # 字典中最长词数

    def MMseg(self, text, dict): # 正向最大匹配算法
        result = []
        index = 0
        text_length = len(text)
        while text_length > index:
            for size in range(self.window_size + index, index, -1):
                piece = text[index:size]
                if piece in dict:
                    index = size - 1
                    break
            index += 1
            result.append(piece)
        return result

    def RMMseg(self, text, dict): # 逆向最大匹配算法
        result = []
        index = len(text)
        while index > 0:
            for size in range(index - self.window_size, index):
                piece = text[size:index]
                if piece in dict:
                    index = size + 1
                    break
            index = index - 1
            result.append(piece)
        result.reverse()
        return result

    def main(self, text, r1, r2):
    # 任务：完成双向最大匹配算法的代码描述
    # ********** Begin *********#
        r1_count=0
        r2_count=0
        if len(r1)>len(r2):
            print(r2,end="")
        elif len(r1)<len(r2):
            print(r1,end="")
        else:
            for i in r1:
                if len(i)==1:
                    r1_count=r1_count+1
            for j in r2:
                if len(j)==1:
                    r2_count=r2_count+1
            if r1_count==r2_count:
                print(r1,end="")
            elif r1_count>r2_count:
                print(r2,end="")
            else:
                print(r1,end="")
    # ********** End **********#

