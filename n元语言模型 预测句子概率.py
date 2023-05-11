import jieba
from collections import Counter
jieba.setLogLevel(jieba.logging.INFO)
#将句子变为"BOSxxxxxEOS"这种形式
def reform(sentence):
    #如果是以“。”结束的则将“。”删掉
    if sentence.endswith("。"):
        sentence=sentence[:-1]
    #添加起始符BOS和终止符EOS
    sentence_modify1=sentence.replace("。", "EOSBOS")
    sentence_modify2="BOS"+sentence_modify1+"EOS"
    return sentence_modify2
#分词并统计词频
def segmentation(sentence,ori_dict):
    jieba.suggest_freq("BOS", True)
    jieba.suggest_freq("EOS", True)
    sentence = jieba.cut(sentence,HMM=False)
    format_sentence=",".join(sentence)
    #将词按","分割后依次填入数组word_list[]
    lists=format_sentence.split(",")
    #统计词频，如果词在字典word_dir{}中出现过则+1，未出现则=1
    if ori_dict!=None:
        for word in lists:
            if word not in ori_dict:
                ori_dict[word]=1
            else:
                ori_dict[word]+=1
    return lists
#比较两个数列，二元语法
def compareList(ori_list,test_list):
    #申请空间
    count_list=[0]*(len(test_list))
    #遍历测试的字符串
    for i in range(0,len(test_list)-1):
        #遍历语料字符串，且因为是二元语法，不用比较语料字符串的最后一个字符
        for j in range(0,len(ori_list)-1):
            #如果测试的第一个词和语料的第一个词相等则比较第二个词
            if test_list[i]==ori_list[j]:
                if test_list[i+1]==ori_list[j+1]:
                    count_list[i]+=1
    return count_list
#计算概率
def probability(test_list,count_list,ori_dict):
    flag=0
    #概率值为p
    p=1
    del test_list[-1]
    for key in test_list:
        p*=(float(count_list[flag])/float(ori_dict[key]))
        flag+=1
    return p
if __name__ == "__main__":
    #语料句子
    sentence_ori="研究生物很有意思。他大学时代是研究生物的。生物专业是他的首选目标。他是研究生。"
    ori_list=[]
    ori_dict={}
    sentence_ori_temp=""
    #测试句子
    sentence_test=input()
    sentence_test_temp=""
    test_list=[]
    ori_dict2={}
    count_list=[]
    p=0
    #分词并将结果存入一个list，词频统计结果存入字典
    sentence_ori_temp=reform(sentence_ori)
    ori_list=segmentation(sentence_ori_temp,ori_dict)
    #print(ori_list)
    sentence_test_temp=reform(sentence_test)
    test_list=segmentation(sentence_test_temp,ori_dict=None)
    #print(test_list)
    count_list=compareList(ori_list, test_list)
    #print(count_list)
    p=probability(test_list,count_list,ori_dict)
    print(p)