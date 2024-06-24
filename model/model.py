import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from pathlib import Path

# paths to data
pathLaptopUbuntu = "/home/ojdwa/NUCmonitor/data/"
pathLaptopVS = "NUCmonitor\data"
pathNuc = "/home/ubuntu/NUCmonitor/data"

# model parameters
n_neighbors = 4
splitseed = 42

def loadData(path):
  pathObj = Path(path)
  return pd.DataFrame([pd.read_json(p, typ="series") for p in pathObj.iterdir()])

def getTargets(data):
  return data["PDU power"]

def getFeatures(data):
  return data.drop(["PDU power"], axis=1)

# Get data
data = loadData(pathLaptopUbuntu)
print(data.head())
X = getFeatures(data)
y = getTargets(data)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=splitseed)

# models
models = { "Friedman Tree     "  : DecisionTreeRegressor(ccp_alpha=1, criterion="friedman_mse", splitter="best"),
           "MLP Regressor     "  : MLPRegressor(hidden_layer_sizes=[5, 10 ,5], activation="logistic", learning_rate="adaptive", early_stopping=True),
           "Kernel Ridge      "  : KernelRidge(alpha=0.8),
           "Linear Regression "  : LinearRegression(),
           "Random Forest     "  : RandomForestRegressor(),
           "KNN               "  : KNeighborsRegressor(n_neighbors=n_neighbors, weights="distance") }
for name, model in models.items():
  print(name)
  model.fit(X_train, y_train)
  y_pred = model.predict(X_test)
  mse = mean_squared_error(y_test, y_pred)
  if mse < 1:
    print("Predictions:", y_pred.head())
    print("Actuals    :", y_test.head())
  print("MSE:", mse, "\n")
