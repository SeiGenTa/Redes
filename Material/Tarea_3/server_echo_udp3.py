#!/usr/bin/python3
# Version trivial del servidor de eco UDP: por cada paquete recibido
# lo respondo al enviador
import os, signal
import sys, threading
import socket, jsockets
import struct

s = jsockets.socket_udp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    data, addr = s.recvfrom(1024)
    if not data:
        continue
    print(data)
    s.sendto(data, addr)
