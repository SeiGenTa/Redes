#!/usr/bin/python3
# Echo server program 
# Usando select para multi-clientes, version simple: bad_client me mata
import select
import os, signal
import sys
import jsockets

Sock = jsockets.socket_tcp_bind(1818)
if Sock is None:
    print('could not open socket')
    sys.exit(1)
# Sock.setblocking(0) # revisar si es necesario

inputs = [Sock]

while inputs:
    readable,writable,exceptional = select.select(inputs,[],inputs)
    for s in exceptional: # cerramos sockets con error
        print('Cliente desconectado (error)')
        inputs.remove(s)
        s.close()
    for s in readable:
        if s is Sock:
            conn, addr = s.accept()
            print(f'Cliente conectado desde {addr}')
            inputs.append(conn)
        else: # leo datos del socket
            data = s.recv(1024)
            if not data: # EOF, cliente se desconectó
                print('Cliente desconectado')
                inputs.remove(s)
                s.close()
            else: # Hago eco como debe ser
                s.send(data)
