import paramiko
import time

class PDU:

  def __init__(self, pduIP, username, password, outlet):
    self.hostname = pduIP
    self.username = username
    self.password = password
    self.outlet = outlet

  # currently starts new SSH session for each read, inefficient try to fix
  def getOutletPower(self, outlet):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=self.hostname, username=self.username, password=self.password)
    _, stdout, _ = client.exec_command("olReading " + self.outlet + " power")
    return stdout.readline()

pdu = PDU("10.68.17.123", "apc", "apc", "6")
print(pdu.getOutletPower("6"))
print(pdu.getOutletPower("7"))


