from monitoringTool import NUCmonitor
import os

# not currently used
import subprocess

# PLAN: laptop drives stress-ng and iperf commands

def gen(dirPath, pduIP, pduUn, pduPw, pduOl):
  print("Data generation for directory:", dirPath)
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  i = 0
  nucMonitor = NUCmonitor(pduIP, pduUn, pduPw, pduOl)
  while True:
    stats = nucMonitor.monitor()
    fPath = dirPath + str(i) + ".json"
    nucMonitor.toJson(stats, dirPath + str(i) + ".json")
    if i % 10 == 0:
      print(stats)
    i += 1

dirPath = "/home/ubuntu/NUCmonitor/data/"
gen(dirPath, "10.68.17.123", "apc", "apc", "6")
