import time
import json
import os
import pduSsh

class NUCmonitor:

  def __init__(self, pduIP, pduUsername, pduPassword, pduOutlet):
    self.pduIP = pduIP
    self.pduUsername = pduUsername
    self.pduPasspord = pduPassword
    self.pduOutlet = pduOutlet

  def connectToPdu():
    self.pdu = PDU(self.pduIP, self.pduUsername, self.pduPassword)
    power = self.pdu.getOutletPower(self.pduOutlet)
    self.pdu.close()
    return power

  def readCpuEnergy():
    with open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r") as file:
      return float(file.read())

  def readCpuTemp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
      return {"CPU temp": float(file.read()) / 1000 }

  #
  # This recieves the average values over 1, 5 and 15 minutes and is not helpful for this case
  # The driving script only invokes stress-ng for times < 1min so there is little change to these stats
  # Hence these stats wont make good features for the model
  #
  def readCpuLoad():
    with open("/proc/loadavg") as file:
      stats = file.read()
      return {"CPU load (/proc/loadavg)(1m)": float(stats.split()[0]),
	      "CPU load (/proc/loadavg)(5m)": float(stats.split()[1]),
	      "CPU load (/proc/loadavg)(15m)": float(stats.split()[2])}

  # Another way of finding INSTANTANEOUS cpu load is using /proc/stat
  def readCpuLoadII():
    with open("/proc/stat") as file:
      topLine = file.readline()
    # output list: [user, nice, system, idle]
      out = [int(x) for x in topLine.split()[1:5]]
    return out

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

  def calcCpuLoadII(l0, l1):
    return {"CPU load (/proc/stat)(1s)": float( sum(l1[0:3]) - sum(l0[0:3]) ) / float( sum(l1) - sum(l0) ) }

  def calcIfDatarates(s0, s1, t):
    out = {}
    for i in range(len(s0)):
      out.update({s0[i][0]+" RX": (s1[i][1] - s0[i][1]) / t } )
      out.update({s0[i][0]+" TX": (s1[i][2] - s0[i][2]) / t } )
    return out

# all time restrained operations in here to keep reporting interval close to intended
  def monitor(interval=1.0):
    # first readings
    cpuEnergy0 = NUCmonitor.readCpuEnergy()
    ifStats0 = NUCmonitor.readIfStats()
    cpuLoadII0 = NUCmonitor.readCpuLoadII()
    # sleep
    time.sleep(interval)
    # second readings
    cpuEnergy1 = NUCmonitor.readCpuEnergy()
    ifStats1 = NUCmonitor.readIfStats()
    cpuLoadII1 = NUCmonitor.readCpuLoadII()
    cpuTemp = NUCmonitor.readCpuTemp()
    # cpuLoad = NUCmonitor.readCpuLoad()
    # calculate
    cpuPower = NUCmonitor.calcCpuPower(cpuEnergy0, cpuEnergy1, interval)
    ifDatarates = NUCmonitor.calcIfDatarates(ifStats0, ifStats1, interval)
    cpuLoadII = NUCmonitor.calcCpuLoadII(cpuLoadII0, cpuLoadII1)
    # append
    out = {}
    out.update(cpuTemp)
    out.update(cpuLoad)
    out.update(cpuLoadII)
    out.update(cpuPower)
    out.update(ifDatarates)
    return out

  def toJson(obj, path="/home/ubuntu/NUCmonitor/nucMonitor/test.json"):
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

# toJson(monitor())
nucMonitor = NUCmonitor(pduIP="10.68.17.123", pduUsername="apc", pduPassword="apc", pduOutlet="6")
print(nucMonitor.monitor())
