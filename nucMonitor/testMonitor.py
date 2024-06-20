from monitoringTool import NUCmonitor
import time

# Periodically reports stats gathered by monitoring tool
def report():
  nucMonitor = NUCmonitor("10.68.17.50", "apc", "apc", "6")
  while True:
    print(nucMonitor.monitor())
    time.sleep(1)

report()
