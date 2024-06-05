import paramiko
import time

def sshNUC(serverIP):
  ssh_client = paramiko.SSHClient()
  print("Client initialised")

  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  print("Set policies")
  ssh_client.connect(hostname='10.68.98.205', username='ubuntu', password='ubuntu')
  print("Connection made")
  stdin, stdout, stderr = ssh_client.exec_command("stress-ng --cpu 0")
  print("Started stress")
  input("Proceed?")
  stdin, stdout, stderr = ssh_client.exec_command("killall stress-ng")
  print("Killed stress processes")
  ssh_client.close()
  print("Client closed")
  return stdout.read()

serverIP = "ubuntu@10.68.98.205"
print(sshNUC(serverIP))
