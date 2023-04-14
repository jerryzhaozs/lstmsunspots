import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Import the sunspot data
data = pd.read_csv('C:/Users/Administrator/Desktop/lstm/sunspots/sunspot_data.csv', parse_dates=[0], index_col=[0], header=None, names=['Date', 'Monthly Mean Total Sunspot Number'])
print(data)
# Prepare the data for the LSTM model
def prepare_data(data, n_in=1, n_out=1):
    X, y = [], []
    for i in range(len(data)-n_in-n_out):
        X.append(data[i:i+n_in])
        y.append(data[i+n_in:i+n_in+n_out])
    return np.array(X), np.array(y)

n_steps = 12
train_data = data[:int(len(data)*0.8)]
test_data = data[int(len(data)*0.8):]
train_X, train_y = prepare_data(train_data['Monthly Mean Total Sunspot Number'].values, n_steps)
test_X, test_y = prepare_data(test_data['Monthly Mean Total Sunspot Number'].values, n_steps)

# Define the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(n_steps, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Train the LSTM model
model.fit(train_X, train_y, epochs=100, batch_size=16, validation_data=(test_X, test_y), verbose=0)

# Predict on the test set
test_pred = model.predict(test_X)

# Plot the results
plt.plot(test_data.index[n_steps:], test_data['Monthly Mean Total Sunspot Number'][n_steps:], label='Actual')
plt.plot(test_data.index[n_steps:], test_pred[:,0], label='Predicted')
plt.legend()
plt.show
