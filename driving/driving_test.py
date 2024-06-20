import paramiko
import subprocess
import pytest

from NUCmonitor.monitoring.NUC import NUC_IP, NUC_UN, NUC_PW
from NUCmonitor.monitoring.PDU import PDU

#
# testpy script automating the generation of client-side iperf traffic.
# Runs successive iperf -c commands with different options, covering cartesian product of p_option s
# -d dualtest	bi-directional
# -r tradeoff	server connects back to the client
# -p parallel	parallel connections, to ensure maximal loading of interface
# -S ToS	type of service
#	0x10	min delay
#	0x08	max throughput
#	0x04	max reliability
#	0x02	min cost
#

# Builds and executes iperf command
def iperfCmd(serverIP, dualtest=False, tradeoff=False, parallel=0, tos=0, udp=False, bitrate=0, length=0):
  # adaptable
  args = ["iperf", "-c", serverIP]
  if dualtest:
    args.append("-d")
  if tradeoff:
    args.append("-r")
  if parallel:
    args.append("-P")
    args.append(str(parallel))
  if tos:
    args.append("-S")
    args.append(str(tos))
  if udp:
    args.append("-u")
  if bitrate:
    args.append("-b")
    args.append(str(bitrate))
  if length:
    args.append("-l")
    args.append(str(length))
  print(" ".join(args))
  subprocess.run(args)

# Opens an SSH connection to the NUC
def driveStress(serverIP, username, password, stress):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(hostname=serverIP, username=username, password=password)
  client.exec_command("stress-ng -c 0 -l " + str(stress))
  return client

# Remotely kills all stress-ng processes on the NUC
def stopStress(client):
  client.exec_command("killall stress-ng")
  client.close()

def closeSsh(client):
  client.close()

# iperf option parameters
p_dualtest = [False, True]
p_tradeoff = [False, True]
p_parallel = [1, 4, 8, 12]
p_tos = [0x08]
p_stress = [0, 20, 40, 60, 80]

@pytest.fixture(params=p_dualtest)
def dualtest(request):
  return request.param

@pytest.fixture(params=p_tradeoff)
def tradeoff(request):
  return request.param

@pytest.fixture(params=p_parallel)
def parallel(request):
  return request.param

@pytest.fixture(params=p_tos)
def tos(request):
  return request.param

@pytest.fixture(params=p_stress)
def stress(request):
  return request.param

# Run tests
# At the moment, a new client is initialised and a new SSH connection initiated for each test case
# This is ihighly inefficient, instead initialise the SSH connection at the begin of the test.
# This can be achieved wihtin the pytest framework using test config file
# If this is implemented the config script can also invoke 'iperf -s -D' on the NUC, meaning all stimuli and driving for generating data is done on another device, and the NUC only has to record its data
def test(dualtest, tradeoff, parallel, tos, stress):
  if stress:
    nucClient = driveStress(NUC_IP, NUC_UN, NUC_PW, stress)
  iperfCmd(NUC_IP, dualtest=dualtest, tradeoff=tradeoff, parallel=parallel, tos=tos)
  if stress:
    stopStress(nucClient)
  pass

test(False, False, 1, 0x08, 20)