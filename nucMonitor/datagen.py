from monitoringTool import *
import os
import subprocess

def gen(testId):
  print("Data generation for test ID:", testId)
  dirPath = "/home/ubuntu/NUCmonitor/testData" + str(testId) + "/"
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  print("Data points will be stored as json at", dirPath)
  i = 0
  while True:
    stats = monitor()
    print("Data point:", i)
    stats.update({"System power": float(input("Input power reading: "))})
    fPath = dirPath + str(i) + ".json"
    toJson(stats, fPath)
    i += 1

gen(0)
