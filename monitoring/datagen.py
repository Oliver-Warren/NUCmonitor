from NUC import NUC
from PDU import PDU_IP, PDU_UN, PDU_PW, PDU_OL
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
