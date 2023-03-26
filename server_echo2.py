#!/usr/bin/python3
# Echo server program - version of server_echo2_n.c
# Usando procesos para multi-clientes
import os, signal
import sys
import jsockets

def childdeath(signum, frame):
  os.waitpid(-1, os.WNOHANG)

def server(conn):
    print('Cliente conectado')
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
    pid = os.fork()
    if pid == 0:
        s.close()
        server(conn)
        sys.exit(0)
    else:
        conn.close();
