# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:00:58 2022

@author: Administrator
"""

import torch

#%%

x=torch.randn(3,requires_grad=True)
print(x)

y=x+2
print(y)
z=y*y*2
z=z.mean()
print(z)

z.backward() # dz/dx
print(x.grad)

#%%

x=torch.randn(3, requires_grad=True)
print(x)
## Prevent from tacking gradient:
# x.requires_grad_(False)
# x.detach()
# with torch.no_grad():
#     pass

"""1"""
# x.requires_grad_(False)
# print(x)
"""2"""
# y=x.detach()
# print(y)
"""3"""
# with torch.no_grad():
#     y=x+2
#     print(y)

#%% A dummy traning example for test

weights = torch.ones(4,requires_grad=True)

for epoch in range(2):  #if we have two iterations
    model_output = (weights*4).sum()
    
    model_output.backward()
    
    print(weights.grad)
    
    weights.grad.zero_()
    '''During our taining step
       Be aware of empty the gradient of weights'''

#%% Optimizer

weights = torch.ones(4,requires_grad=True)
"""
    SGD for stochastic gradient descent
"""
optimizer = torch.optim.SGD(weights, lr=0.01)
optimizer.step()
optimizer.zero_grad() # Empty the gradient






































