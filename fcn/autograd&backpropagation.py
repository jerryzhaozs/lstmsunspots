# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:32:06 2022

@author: Administrator
"""

"""
Prediction: PyTorch Model
Gradients: Computation Autograd
Loss Computation: PyTorch Loss
Parameter updates: PyTorch optimizer
"""
import numpy as np
import torch
X=torch.tensor([1,2,3,4],dtype=torch.float32)
Y=torch.tensor([2,4,6,8],dtype=torch.float32)

w=torch.tensor(0.0,dtype=torch.float32,requires_grad=True)

# Calculate prediction
def forward(x):
    return w*x

# loss = MSE
def loss(y,y_predicted):
    return ((y-y_predicted)**2).mean()


# Gradient
# MSE=1/N*(w*x-y)**2
# dJ/dw=1/N 2x (w*x-y)
def gradient(x,y,y_predicted):
    return np.dot(2*x,y_predicted-y).mean()
# def gradient(x,y,y_predicted):
    

print(f'Prediction before training: f(6)={forward(6):.3f}')

# Training
learning_rate=0.01
n_iters=20

for epoch in range(n_iters):
    # Prediction = forward pass
    y_pred=forward(X)
    
    # Loss
    l=loss(Y,y_pred)
    
    # Gradient
    l.backward() # dl/dw
    
    # Update weights
    with torch.no_grad():
        w-=learning_rate*w.grad
        
    #zero gradient
    w.grad.zero_()
    
    if epoch %1 == 0:
        print(f'epoch {epoch+1}: w={w:.3f}, loss={l:.8f}')


print(f'Prediction after the training: f(6)={forward(6):.3f}')
















