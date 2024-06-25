import paramiko

PDU_IP = "10.68.17.123"
PDU_UN = "apc"
PDU_PW = "apc"
PDU_OL = "6"

class PDU:

  def __init__(self, pduIP=PDU_IP, username=PDU_UN, password=PDU_PW, outlet=PDU_OL):
    self.hostname = pduIP
    self.username = username
    self.password = password
    self.outlet = outlet

  # currently starts new SSH session for each read, inefficient try to fix
  def getOutletPower(self):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
      try:
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        _, stdout, _ = client.exec_command("olReading " + self.outlet + " power")
        return float(stdout.readline().split()[3])
      except: Exception
            