from monitoringTool import *
import os
import subprocess

def stressCmd(load=50, cores=3):
  args = ["stress-ng", "--daemon", "1", "-q", "-c", str(cores), "-l", str(load)]
  print(" ".join(args))
  subprocess.run(args)

def gen(testId):
  print("Data generation for test ID:", testId)
  dirPath = "/home/ubuntu/monitoringTool/test" + str(testId) + "/"
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

# gen(0)
stressCmd()
print(monitor())
