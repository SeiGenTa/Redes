#!/usr/bin/python3
# Echo server program - version of server_echo2.5_n.c
# Usando procesos para multi-clientes, con MAX_PROCS maximo de clientes a la vez
import os, signal
import sys
import jsockets

MAX_PROCS = 10
chld_cnt = 0

def childdeath(signum, frame):
  global chld_cnt
  os.waitpid(-1, os.WNOHANG)
  chld_cnt -= 1

def server(conn):
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
    conn.close()
    print('Cliente desconectado')
    sys.exit(0)
    

signal.signal(signal.SIGCHLD, childdeath)
s = jsockets.socket_tcp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept();
    print('Cliente '+str(chld_cnt)+' conectado')
    if chld_cnt >= MAX_PROCS:
        conn.close()
        continue

    pid = os.fork()
    if pid == 0:
        s.close()
        server(conn)
        sys.exit(0)
    else:
        chld_cnt += 1
        conn.close();
