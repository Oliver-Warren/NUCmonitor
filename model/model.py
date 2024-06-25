import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from pathlib import Path
from pickle import dump

# paths to data
pathLaptopUbuntu = "/home/ojdwa/NUCmonitor/data/"
pathLaptopVS = "NUCmonitor\data"
pathNuc = "/home/ubuntu/NUCmonitor/data"

# model parameters
n_neighbors = 20
splitseed = 42

def loadData(path):
  pathObj = Path(path)
  return pd.DataFrame([pd.read_json(p, typ="series") for p in pathObj.iterdir()])

def getTargets(data):
  return data["PDU power"]

def getFeatures(data):
  return data.drop(["PDU power", "lo RX", "lo TX", "wlp2s0 RX", "wlp2s0 TX"], axis=1)
  
# get features (X) and targets (y) from file system
def getData(path):
  data = loadData(path)
  X = getFeatures(data)
  y = getTargets(data)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=splitseed)
  return X, y, X_train, X_test, y_train, y_test

# try some different models
def tryModels(X_train, X_test, y_train, y_test):
  models = { "Friedman Tree       "  : DecisionTreeRegressor(ccp_alpha=1, criterion="friedman_mse", splitter="best"),
             "MLP Regressor       "  : MLPRegressor(hidden_layer_sizes=[100, 50], activation="logistic", learning_rate="adaptive", early_stopping=True),
             "Kernel Ridge        "  : KernelRidge(alpha=0.8),
             "Linear Regression   "  : LinearRegression(),
             "Random Forest       "  : RandomForestRegressor(),
             "KNN                 "  : KNeighborsRegressor(n_neighbors=n_neighbors, weights="distance"),
             "Logistic Regression "  : LogisticRegression(penalty="l2", fit_intercept=True)}
  for name, model in models.items():
    print(name)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    if mse < 1:
      print("Predictions:", y_pred[0:5])
      print("Actuals    :", list(y_test[0:5]))
    print("MSE:", mse, "\n")

# Linear Regression is the simplest model and shows the most promise
# This method trains a Linear Regression model and stores it as an .onnx serialisation
# The model is trained on the ENTIRE dataset
def makeLinReg(X, y):
  model = LinearRegression().fit(X, y)
  with open("linReg.pkl", "wb") as file:
    dump(model, file, protocol=5)

# script
X, y, X_train, X_test, y_train, y_test = getData(pathLaptopVS)
makeLinReg(X, y)
# tryModels(X_train, X_test, y_train, y_test)


