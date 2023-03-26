#!/usr/bin/python3
# Echo server program 
# Usando select para multi-clientes, version con soporte para bad_client
import select
import os, signal
import sys, errno
import socket
import jsockets

Sock = jsockets.socket_tcp_bind(1818)
if Sock is None:
    print('could not open socket')
    sys.exit(1)
Sock.setblocking(0) # es necesario para que no se bloquee en una escritura si el socket está lleno

inputs = [Sock]
outputs = []
pending_data = {}

while inputs:
    readable,writable,exceptional = select.select(inputs,outputs,inputs)
    for s in exceptional: # cerramos sockets con error
        print('Cliente desconectado (error)')
        inputs.remove(s)
        s.close()
    for s in readable: # sockets con datos para mi
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
                try:
                    s.send(data)
                except socket.error as e:
                    if e.errno != errno.EAGAIN:
                        inputs.remove(s)
                    else:     # socket lleno, espero que se desocupe
                        pending_data[s] = bytearray(data) # hacer una copia para después
                        inputs.remove(s)
                        outputs.append(s)
    for s in writable: # sockets llenos que se desocuparon
        try:
            s.send(pending_data[s])
        except:
            print('send failed')
        pending_data[s] = bytearray()
        outputs.remove(s)
        inputs.append(s)
