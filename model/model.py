import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pathlib import Path

pathLaptop = "/home/ojdwa/NUCmonitor/testData0"
pathNuc = "/home/ubuntu/NUCmonitor/testData0"

# Create data set from the jsons output by monitoringtool
def loadData(path):
  pathObj = Path(path)
  return pd.DataFrame([pd.read_json(p, typ="series") for p in pathObj.iterdir()])

# Return targets (system power consumption)
def getTargets(data):
  return data["System power"]

# Return features (dataset - targets)
def getFeatures(data):
  return data.drop(["System power"], axis=1)

# Load jsons into df
data = loadData(pathLaptop)
print(data.head())

# Separate
X = getFeatures(data)
y = getTargets(data)

# Train-test split
seed = 42 # change to get other splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

# might want to change this to something non-linear
model = LinearRegression()
model.fit(X_train, y_train)

# test
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("MSE:", mse)




