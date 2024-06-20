from monitoringTool import *
import time

# Periodically reports stats gathered by monitoring tool
def report():
  while True:
    print(monitor())
    time.sleep(1)

report()
