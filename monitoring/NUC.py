import time
import json
from PDU import PDU
from pickle import load
from sklearn.linear_model import LinearRegression
import numpy as np
import warnings

TESTPATH  = "/home/ubuntu/NUCmonitor/nucMonitor/test.json"
MODELPATH = "/home/ubuntu/NUCmonitor/model/linReg.pkl"

warnings.simplefilter("ignore")
class NUC:

  def __init__(self, modelOn=False):
    if modelOn:
      self.model = self.loadModel()

  @staticmethod
  def readPduPower():
    return {"PDU power": PDU().getOutletPower()}

  @staticmethod
  def readCpuEnergy():
    with open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r") as file:
      return float(file.read())

  @staticmethod
  def readCpuTemp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
      return {"CPU temp": float(file.read()) / 1000 }

  # Not used for features, not instantaneous load
  @staticmethod
  def readCpuLoad():
    with open("/proc/loadavg") as file:
      stats = file.read()
      return {"CPU load (/proc/loadavg)(1m)": float(stats.split()[0]),
	      "CPU load (/proc/loadavg)(5m)": float(stats.split()[1]),
	      "CPU load (/proc/loadavg)(15m)": float(stats.split()[2])}

  # Used as a feature, instantaneous load
  @staticmethod
  def readCpuLoadII():
    with open("/proc/stat") as file:
      topLine = file.readline()
    # output list: [user, nice, system, idle]
      out = [int(x) for x in topLine.split()[1:5]]
    return out

  @staticmethod
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

  @staticmethod
  def calcCpuPower(e0, e1, t):
    return {"CPU power": ( e1 - e0 ) / ( t * 1000000 ) }

  @staticmethod
  def calcCpuLoadII(l0, l1):
    return {"CPU load (/proc/stat)(1s)": float( sum(l1[0:3]) - sum(l0[0:3]) ) / float( sum(l1) - sum(l0) ) }

  @staticmethod
  def calcIfDatarates(s0, s1, t):
    out = {}
    for i in range(len(s0)):
      out.update({s0[i][0]+" RX": (s1[i][1] - s0[i][1]) / t } )
      out.update({s0[i][0]+" TX": (s1[i][2] - s0[i][2]) / t } )
    return out

  # all time restrained operations in here to keep reporting interval close to intended
  def monitor(self, interval=1.0):
    # first readings
    cpuEnergy0 = self.readCpuEnergy()
    ifStats0 = self.readIfStats()
    cpuLoadII0 = self.readCpuLoadII()
    # sleep
    time.sleep(interval)
    # second readings
    cpuEnergy1 = self.readCpuEnergy()
    ifStats1 = self.readIfStats()
    cpuLoadII1 = self.readCpuLoadII()
    # non-timed readings
    pduPower = self.readPduPower()
    cpuTemp = self.readCpuTemp()
    ### NOT USED cpuLoad = NUCmonitor.readCpuLoad()
    # calculate
    cpuPower = self.calcCpuPower(cpuEnergy0, cpuEnergy1, interval)
    ifDatarates = self.calcIfDatarates(ifStats0, ifStats1, interval)
    cpuLoadII = self.calcCpuLoadII(cpuLoadII0, cpuLoadII1)
    # append
    out = {}
    out.update(cpuTemp)
    ### NOT USED out.update(cpuLoad)
    out.update(cpuLoadII)
    out.update(cpuPower)
    out.update(ifDatarates)
    out.update(pduPower)
    # model 
    try:
      predPower = self.predictPower(out.copy())
      out.update({"Predicted power": predPower})
    except Exception:
      print("Model not loaded")
    return out
  
  @staticmethod
  def loadModel(modelPath=MODELPATH):
    with open(modelPath, "rb") as file:
      model = load(file)
    return model
  
  # Highly custom at the moment, not portable
  # This is because have to form a dataframe similar to the one the model is trained on
  def predictPower(self, features, omitList=["lo RX", "lo TX", "wlp2s0 RX", "wlp2s0 TX", "PDU power"]):
    if self.model == None:
      raise Exception()
    else:
      # remove feautures that aren't used by the model
      for label in omitList:
        features.pop(label)
      return float(self.model.predict(np.array([float(x) for x in features.values()]).reshape(1, -1)))

  @staticmethod
  def toJson(obj, path=TESTPATH):
    jsonObj = json.dumps(obj, indent=4)
    with open(path, "w") as file:
      file.write(jsonObj)

# nuc = NUC(modelOn=True)
# print(nuc.monitor())

