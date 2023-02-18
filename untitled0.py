# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:16:11 2023

@author: Administrator
"""

from numpy import array
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
import copy
from statsmodels.tsa.stattools import pacf
import matplotlib.pyplot as plt
from sklearn import preprocessing


aa=[1,2,3,4,5,6,7,8,20,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,19,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,21,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,20,1,2,3,4,5,6,7,8,9]
aaa=copy.deepcopy(aa)
xmin = min(aa) 
xmax=max(aa)
for i, x in enumerate(aaa):
    aaa[i] = (x-xmin) / (xmax-xmin)

series = array(aaa)
n_features = 1
series = series.reshape((len(series), n_features))

n_input =18
endd=len(aaa)-1
plt.plot(aaa[0:n_input])
# bb=aaa[endd-n_input:endd]
bb=aaa[0:n_input]
len(bb)
plt.plot(bb)


# define generator
generator = TimeseriesGenerator(series, series, length=n_input, batch_size=1)
# define model
model = Sequential()
model.add(LSTM(units =256, activation = 'tanh', recurrent_activation ='hard_sigmoid', input_shape=(n_input, n_features)))
model.add(Dense (units =1, activation = 'linear'))
model.compile ( loss ='mean_squared_error',optimizer = 'rmsprop')
# fit model
model.fit(generator, steps_per_epoch=1, epochs=100, verbose=2,shuffle = True)

#%%
origin_input=copy.deepcopy(bb)
ans=copy.deepcopy(bb)
for i in range(0,200):
    now_input=array(origin_input).reshape((1, n_input, n_features))
    yhat = model.predict(now_input, verbose=0)
    # print(i,yhat[0][0])
    ans.append(yhat[0][0])
    origin_input.remove(origin_input[0])
    origin_input.append(yhat[0][0])
plt.plot(ans)