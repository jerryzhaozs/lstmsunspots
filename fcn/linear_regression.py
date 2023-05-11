# 1) Design model (input,output size, forward pass)
# 2) Construct loss and optimizer
# 3) Training loop:
#  -
import random

import torch
import torch.nn as nn
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt

# 0) prepare data
X_numpy, y_numpy = datasets.make_regression(n_samples=100
                                            , n_features=1
                                            , noise=20
                                            , random_state=1)

X_train = torch.from_numpy(X_numpy.astype(np.float32))
y_train = torch.from_numpy(y_numpy.astype(np.float32))
y_train = y_train.view(y_train.shape[0], 1)  # reshape

n_sample, n_features = X_train.shape

# 1) model
input_size = n_features
output_size = 1
model = nn.Linear(input_size, output_size, dtype=torch.float32)

# 2) loss and optimizer Mean Square Error
learning_rate=0.01
criterion=nn.MSELoss()
optimizer=torch.optim.SGD(model.parameters(),lr=learning_rate)

# 3) training loop
n_epochs=1000
for epoch in range(n_epochs):
    # forward pass : loss and preditcion
    y_pred=model(X_train)
    loss=criterion(y_train,y_pred)

    # backward pass : gradient
    loss.backward()

    # update
    optimizer.step()

    # empty gradient
    optimizer.zero_grad()

    if(epoch%10==0):
        print(f'epoch{epoch}: loss:{loss.item()}')

predicted = model(X_train).detach().numpy()
plt.plot(X_numpy,y_numpy,'ro')
plt.plot(X_numpy,predicted,'b')
plt.show()