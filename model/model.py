# This file contains the model training and testing scripts

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Create data set from the jsons output by monitoringtool
def loadData():
  return

# Return targets (system power consumption)
def getTargets(data):
  return

# Return features (dataset - targets)
def getFeatures(data):
  return

# Training script
data = loadData()
X = getFeatures(data)
y = getTargets(data)

# print(X.head())
# print(Y.head())

# train test split
seed = 42 # change for other splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, randomstate=seed)

# might want to change this to something non-linear
model = LinearRegression()
model.fit(X_train, y_train)

# test
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("MSE:", mse)




