import time
import json
import os

def readCpuEnergy():
  with open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r") as file:
    return float(file.read())

def readCpuTemp():
  with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
    return {"CPU temp": float(file.read()) / 1000 }

def readCpuLoad():
  with open("/proc/loadavg") as file:
    return {"CPU load": float(file.read().split()[0])}

def readIfStats():
  ifNames = []
  txBytes = []
  rxBytes = []
  with open("/proc/net/dev", "r") as file:
    for line in file.readlines()[2:]:
      ifNames.append(line.split()[0].replace(":", ""))
      rxBytes.append(float(line.split()[1]))
      txBytes.append(float(line.split()[9]))
  return list(zip(ifNames, rxBytes, txBytes))

def calcCpuPower(e0, e1, t):
  return {"CPU power": ( e1 - e0 ) / ( t * 1000000 ) }

def calcIfDatarates(s0, s1, t):
  out = {}
  for i in range(len(s0)):
    out.update({s0[i][0]+" RX": (s1[i][1] - s0[i][1]) / t } )
    out.update({s0[i][0]+" TX": (s1[i][2] - s0[i][2]) / t } )
  return out

# all time restrained operations in here to keep reporting interval close to intended
def monitor(interval=1.0):
  # first readings
  cpuEnergy0 = readCpuEnergy()
  ifStats0 = readIfStats()
  # sleep
  time.sleep(interval)
  # second readings
  cpuEnergy1 = readCpuEnergy()
  ifStats1 = readIfStats()
  cpuTemp = readCpuTemp()
  cpuLoad = readCpuLoad()
  # calculate
  cpuPower = calcCpuPower(cpuEnergy0, cpuEnergy1, interval)
  ifDatarates = calcIfDatarates(ifStats0, ifStats1, interval)
  # append
  out = {}
  out.update(cpuTemp)
  out.update(cpuLoad)
  out.update(cpuPower)
  out.update(ifDatarates)
  return out

def toJson(obj, path="/home/ubuntu/monitoringTool/test.json"):
  jsonObj = json.dumps(obj, indent=4)
  with open(path, "w") as file:
    file.write(jsonObj)

def experiment(tests, trial):
  dirPath = "/home/ubuntu/monitoringTool/trial" + str(trial) + "/"
  os.makedirs(os.path.dirname(dirPath), exist_ok=True)
  for i in range(tests):
    result = monitor()
    print("TRIAL", trial, "Test", i)
    result.update({"System power": input("System power for test" + str(i) + ": ")})
    print(result)
    path = dirPath + "test" + str(i) + ".json"
    toJson(result, path)
    input("Proceed?")