from NUC import NUC
import time

# Periodically reports NUC stats
def report(interval=1.0):
  nuc = NUC(modelOn=True)
  while True:
    print(nuc.monitor())
    time.sleep(interval)

report()