#!/usr/bin/python3
# Echo server program - version of server_echo4_n.c
# Usando threads para multi-clientes
import os, signal
import sys, threading
import jsockets

class ClientThread(threading.Thread):
    def __init__(self, addr, s):
        threading.Thread.__init__(self)
        self.sock = s
    def run(self):
        print('Cliente Conectado')
        
        while True:
            data = self.sock.recv(1024)
            if not data: break
            print('serv read')
            self.sock.send(data)
            print('serv write')
        self.sock.close()
        print('Cliente desconectado')
    
s = jsockets.socket_tcp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept();
    newthread = ClientThread(addr, conn)
    newthread.start()
