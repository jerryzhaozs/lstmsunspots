# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:13:02 2022

@author: Administrator
"""
#%% Import Part
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

#%% Import Datasets
mnist = keras.datasets.mnist

(x_train,y_train),(x_test,y_test)=mnist.load_data()

print(x_train.shape,y_train.shape)

#%% Normalize: 0,255 -> 0,1
x_train,x_test = x_train/255.0,x_test/255.0

#%% Plot the Data
for i in range(6):
    plt.subplot(2,3,i+1)
    plt.imshow(x_train[i],cmap='gray')
plt.show()

#%% Model
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128,activation='relu'),
    keras.layers.Dense(10),
])

print(model.summary())