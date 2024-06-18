import paramiko

class PDU:

  def __init__(self, pduIP, username, password):
    self.pduIP = pduIP
    self.username = username

    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    self.client.connect(hostname=pduIP, username=username, password=password)

  def getOutletPower(outlet):
    _, stdout, _ = self.client.exec_command("olReading " + str(outlet) + " power")
    return stdout.readline()

  def close():
    self.client.close()

pduIP = "10.68.17.123"
username = "apc"
password = "apc"

outlet = "6"

pdu = PDU(pduIP, username, password)
print(pdu.getOutletPower(outlet))
close()
