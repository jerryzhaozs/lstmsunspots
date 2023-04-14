# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:16:11 2023

@author: Administrator
"""
import math
for i in range(100000):
    # 转化为整型值
    x = int(math.sqrt(i + 100))
    y = int(math.sqrt(i + 255))
    if(x * x == i + 100) and (y * y == i + 255):     # 如果一个数的平方根的平方等于该数，这说明此数是完全平方数
        print(i)



a='acgweg'
print(len(a))