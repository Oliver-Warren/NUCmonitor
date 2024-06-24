import json
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

from pathlib import Path

pathLaptopUbuntu = "/home/ojdwa/NUCmonitor/data/"
pathLaptopVS = "NUCmonitor\data"
pathNuc = "/home/ubuntu/NUCmonitor/data"

# Create data set from the jsons output by monitoringtool
def loadData(path):
  pathObj = Path(path)
  return pd.DataFrame([pd.read_json(p, typ="series") for p in pathObj.iterdir()])

# Return targets (system power consumption)
def getTargets(data):
  return data["PDU power"]

# Return features (dataset - targets)
def getFeatures(data):
  return data.drop(["PDU power"], axis=1)

# Load jsons into df
data = loadData(pathLaptopUbuntu)
print(data.head())

# Separate
X = getFeatures(data)
y = getTargets(data)

#
# For KNN
#
n_neighbors = 15


# Train-test split, now moved into seed loop
# seed = 5 # change to get other splits
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

# might want to change this to something non-linear
for seedP in range(200):

  # model parameters:
  # criterion - friedman_mse worked well
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seedP)

  model = DecisionTreeRegressor(ccp_alpha=1, random_state=seedP, criterion="friedman_mse", splitter="random")
  model.fit(X_train, y_train)
  y_predP = model.predict(X_test)
  mse = mean_squared_error(y_test, y_predP)
  if mse > 2:
    continue
  else:
    # save predicted vs actuals as a csv for analysis
    print("Seed:", seedP, "MSE:", mse, "Typical error:", np.sqrt(mse))
    continue

print("\nKNN\n")
model2 = KNeighborsRegressor(n_neighbors=n_neighbors, weights="distance")
model2.fit(X_train, y_train)

# test
y_predK = model2.predict(X_test)
print("Targets:\n", y_test[:5])
print("Predicted:", y_predK[:5])

mseK = mean_squared_error(y_test, y_predK)
print("MSE:", mse)




