from monitoringTool import *
import os
import subprocess

def gen(dirPath):
  print("Data generation for directory:", dirPath)
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  i = 0
  while True:
    stats = monitor()
    print("Data point:", i)
    stats.update({"System power": float(input("Input power reading: "))})
    fPath = dirPath + str(i) + ".json"
    toJson(stats, fPath)
    i += 1

dirPath = "/home/ubuntu/NUCmonitor/data/realData0/"
gen(dirPath)
