from NUCmonitor.monitoring.NUC import NUC
import os

OUTPATH = "/home/ubuntu/NUCmonitor/data/"

def gen(dirPath):
  print("Data generation for directory:", dirPath)
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  i = 0
  nuc = NUC()
  while True:
    stats = nuc.monitor()
    fPath = dirPath + str(i) + ".json"
    nuc.toJson(stats, dirPath + str(i) + ".json")
    i += 1

gen(OUTPATH)
