import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import yfinance as yf
import matplotlib.pyplot as plt

# Descărcăm datele istorice pentru Bitcoin și Ethereum
bitcoin_data = yf.download('BTC-USD', start='2020-01-01', end='2024-01-01')
ethereum_data = yf.download('ETH-USD', start='2020-01-01', end='2024-01-01')

# Utilizăm doar coloana 'Close' pentru predicție
data = bitcoin_data['Close'].values
data = data.reshape(-1, 1)

# Normalizarea datelor
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Crearea setului de date de antrenament
train_data = scaled_data[:int(len(scaled_data) * 0.8)]
test_data = scaled_data[int(len(scaled_data) * 0.8):]

def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data)-time_step-1):
        X.append(data[i:(i+time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 100
X_train, Y_train = create_dataset(train_data, time_step)
X_test, Y_test = create_dataset(test_data, time_step)

# Reshape pentru LSTM [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, Y_train, batch_size=1, epochs=1)

predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# Vizualizarea rezultatelor
train = bitcoin_data[:int(len(bitcoin_data) * 0.8)]
valid = bitcoin_data[int(len(bitcoin_data) * 0.8):]
valid['Predictions'] = predictions

plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()
