import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# load data
df = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sun-spots.csv', usecols=['Date', 'Sunspots'])

# convert Date column to datetime index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# prepare data
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(df.values)

def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:i+time_steps, :]
        Xs.append(v)
        ys.append(y[i+time_steps])
    return np.array(Xs), np.array(ys)

# create train and test sets
train_size = int(len(dataset) * 0.8)
test_size = len(dataset) - train_size
train_data, test_data = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

# create X/y for train and test sets
time_steps = 12
X_train, y_train = create_dataset(train_data, train_data[:, 0], time_steps)
X_test, y_test = create_dataset(test_data, test_data[:, 0], time_steps)

# build LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# fit model
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1, verbose=1)

# plot training/validation loss
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.legend()
plt.show()

# make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# invert predictions
train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform([y_train])
test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform([y_test])

# plot predictions vs actual values
plt.plot(df.index.values[-len(train_predict):], train_predict[:, 0], label='prediction')
plt.plot(df.index.values[-len(train_predict):], y_train[0], label='actual')
plt.plot(df.index.values[-len(test_predict):], test_predict[:, 0], label='prediction')
plt.plot(df.index.values[-len(test_predict):], y_test[0], label='actual')
plt.legend()
plt.show()
