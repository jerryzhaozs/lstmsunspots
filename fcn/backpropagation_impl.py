# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:13:03 2022

@author: Administrator
"""

"""
    1) Forward pass: Compute Loss
    2) Compute local gradients
    3) Backward pass: Compute dLoss / dWeights using the Chain Rule
"""

import torch

#%%

x=torch.tensor(1.0)
y=torch.tensor(2.0)

w=torch.tensor(1.0,requires_grad=True)

# Do the forward pass and computre the loss
y_hat=w*x
loss=(y_hat-y)**2

print(loss)

# Do the backward pass
loss.backward()
print(w.grad)

### update the parameter and do next forward pass and backward pass




































