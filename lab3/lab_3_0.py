# -*- coding: utf-8 -*-
"""Lab_3_0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H6uPUAU6tqfa1QYl_Y2ovhgv-pLd0wY6
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from google.colab import drive

drive.mount("/content/gdrive")
dataset_train = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/Lab3/data-weather-1.csv") 
 

#dataset_train = pd.read_csv('data-weather-2-test.csv')
training_set = dataset_train.iloc[:, 3:4].values
dataset_train.iloc[:, 3:4]

dataset_train.head(100)

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

plt.plot(training_set)
plt.grid()
plt.show()

plt.plot(training_set_scaled)
plt.show()

X_train = []
y_train = []
for i in range(60, 999):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 10, batch_size = 32)

dataset_test = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/Lab3/data-weather-2-test.csv")

real_stock_price = dataset_test.iloc[:, 3:4].values

dataset_total = pd.concat((dataset_train['Temperature (C)'], dataset_test['Temperature (C)']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 260):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'yellow', label = 'Temperature')
plt.plot(predicted_stock_price, color = 'green', label = 'Predicted Temperature')
plt.title('Temperature Prediction')
plt.xlabel('Days')
plt.ylabel('Time')
plt.legend()
plt.show()

