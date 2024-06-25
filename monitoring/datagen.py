from NUC import NUC
import os

OUTPATH = "/home/ubuntu/NUCmonitor/data/"

def gen(dirPath):
  print("Data generation for directory:", dirPath)
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  i = 0
  nuc = NUC(modelOn=False)
  while True:
    stats = nuc.monitor()
    nuc.toJson(stats, dirPath + str(i) + ".json")
    print("Saved:", i)
    i += 1

gen(OUTPATH)
