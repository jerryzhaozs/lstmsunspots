import re
text=input()
list_ret=list()
#任务：完成对text文本的分句并输出结果
# ********** Begin *********#
patten = re.compile('[a-z0-9][\.\?\!]\s|[\.\?\!]$')

l = re.findall(patten,text)
f = re.finditer(patten,text)
index = 0
for i in f:
    if i.span()[0] == len(text)-1:
        list_ret.append(text[index : i.span()[0]])
    else: list_ret.append(text[index : i.span()[0]+1])
    index = i.span()[1]
print(list_ret)
 # ********** End **********#
