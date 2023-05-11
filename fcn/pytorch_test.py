# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:13:42 2022

@author: Administrator
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import torch
import numpy as np

x=torch.rand(3)
x=torch.empty(2,3)
x=torch.ones(3,3,dtype=torch.float16)
x=torch.rand(2,2)
x=torch.tensor([2.5,0.1])
y=torch.tensor([1,1])
x=torch.rand(2,2)
y=torch.rand(2,2)
y.add_(x)

z=x*y

x=torch.rand(5,6)
#%% reshape
y=x.view(-1,2)
print(y)
print(x.dtype)
print(type(x))

#%% numpy and tensor

a=torch.ones(5)
print(a)
b=a.numpy()
print(type(b))
# =============================================================================
# Attention Under CPU enviorment 
# tensor a and numpy b will point to the same memory location
# So be careful here
# =============================================================================

#%% numpy to tensor

a=np.ones(5)
print(a)
b=torch.from_numpy(a)
print(b)
a+=1
print(b)
# =============================================================================
# ditto
# =============================================================================

#%% Create a tensor on GPU if u have one
#  Notice We can't convert a GPU tensor back to numpy
#  So we can move it back to CPU model then convert it 
if torch.cuba.is_available():
    device=torch.device("cuba")
    x=torch.ones(5,device=device)
    y=torch.ones(5)
    y=y.to(device)
    z=y.to("CPU")
    
#%%
# by default requires_grad will be false
x=torch.ones(5,requires_grad=True)
# make it a true if you want to optimize this tensor later
# in the optimization part