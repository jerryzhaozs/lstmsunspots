# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 10:23:10 2022

@author: Administrator
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2" # clear warnings
import tensorflow as tf

#%% Test
# x=tf.eye(3)

# x=tf.random.normal((3,3),mean=0,stddev=100)

# x=tf.constant([1,2,3])
# y=tf.constant([4,5,6])
# z=tf.tensordot(y,x,axes=1)

# x=tf.random.normal((2,2))
# y=tf.random.normal((2,2))
x=tf.constant([[1,2,1],[2,1,1]])
y=tf.constant([[3,1],[2,2],[1,1]])
z=tf.matmul(x,y)
z=x@y
# print(x)
# print(y)
# print(z)


#%% slicing, indexing
x=tf.constant([[1,2,3,4],[5,6,7,8]])
# print(x[0,1])

#%% reshaping
x=tf.random.normal((5,3))
x=tf.reshape(x, (5,-1))
print(x)

#%% to numpy and to tensor
x=tf.random.normal((4,4))
x=x.numpy()
print(type(x))
x=tf.convert_to_tensor(x)
print(type(x))

#%% String tensor
x=tf.constant(["okko","ioio"])
print(x)
print(type(x))

#%% Variable
x=tf.constant([1,2,3])
print(x)
print()
x=tf.Variable([1,2,3])
print(x)











