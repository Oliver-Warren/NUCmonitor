import paramiko

def connectToPDU(pduIP, username, password):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(hostname=pduIP, username=username, password=password)
  return client

def getOutletPower(client, outlet):
  stdin, stdout, stderr = client.exec_command("olReading " + str(outlet) + " power")
  return stdout.readline()

def closePDU(client):
  client.close()

pduIP = "10.68.17.123"
username = "apc"
password = "apc"

outlet = "6"

pdu = connectToPDU(pduIP, username, password)
print(getOutletPower(pdu, outlet))
closePDU(pdu)
