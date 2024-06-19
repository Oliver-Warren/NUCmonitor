import paramiko

class PDU:

  def __init__(self, pduIP, username, password):
    self.pduIP = pduIP
    self.username = username
    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    self.client.connect(hostname=pduIP, username=username, password=password, banner_timeout=5)

  def getOutletPower(self, outlet):
    _, stdout, _ = self.client.exec_command("olReading " + str(outlet) + " power")
    return stdout.readline()

  def close(self):
    self.client.close()
