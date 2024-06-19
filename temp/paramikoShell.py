import paramiko
import time

class ShellHandle:

  def __init__(self):
    pass

  def __del__(self):
    self.client.close()

  def openConnection(self, IP, us, ps):
    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    self.client.connect(hostname=IP, username=us, password=ps)

    self.channel = self.client.get_transport().open_session()

    self.channel.get_pty()
    self.channel.invoke_shell()

  # this method opens an interactive shell
  def runCommand(self, cmd):
    self.channel.send(cmd + "\n")
    # wait for and return output
    time.sleep(0.2)
    while True:
      if self.channel.recv_ready():
        return self.channel.recv(9999)

shell = ShellHandle()
shell.openConnection("10.68.17.123", "apc", "apc")
print(shell.runCommand("olReading 6 power"))
print("attempt 2")
print(shell.runCommand("olReading 6 power"))
del(shell)
