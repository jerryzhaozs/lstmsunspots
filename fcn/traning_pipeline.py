# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 12:58:54 2022

@author: Administrator
"""
# Pipline
# 1 ) Design model (input, output size, forward pass)
# 2 ) Construct loss and the optimizer
# 3 ) Traning loop
#   - forward pass: compute prediction
#   - backward pass: gradients
#   - update weights

import torch
import torch.nn as nn
# Dataset initialization
X_train = torch.tensor([[1], [2], [3], [4]], dtype=torch.float32)
Y_train = torch.tensor([[2], [4], [6], [8]], dtype=torch.float32)
X_test=torch.tensor([5],dtype=torch.float32)

n_samples,n_features=X_train.shape
print(f'n_samples: {n_samples}  and n_features: {n_features}')

input_size=n_features
output_size=n_features

model=nn.Linear(input_size,output_size,dtype=torch.float32)

# dummy version of nn
class LinearRegression(nn.Module):
    def __init__(self,input_dim,output_dim):
        super(LinearRegression,self).__init__()
        # define layers
        self.lin=nn.Linear(input_dim,output_dim)

    def forward(self,X):
        return self.lin(X)

model=LinearRegression(input_size,output_size)

print(f'Before training:{model(X_test).item():.3f}')


# Training
learning_rate = 0.01
n_iters = 200

loss = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(),lr=learning_rate)

for epoch in range(n_iters):
    # prediction = forward pass
    pre_y=model(X_train)

    # loss
    l=loss(Y_train,pre_y)

    # gradient = backward pass
    l.backward() # dl/wd

    # update weights
    optimizer.step()

    # zero gradient
    optimizer.zero_grad()

    if(epoch %10 == 0):
        [w,b]=model.parameters()
        print(f'epoch{epoch+1}: w={w[0][0].item():.3f} and loss={l:.6f}')

print(f'final prediction:{model(X_test).item():.3f}')