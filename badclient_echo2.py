#!/usr/bin/python3
# Bad Echo client program
# Escribe 1 Mb al servidor y nunca escucha de vuelta
import jsockets
import sys

if len(sys.argv) != 3:
    print('Use: '+sys.argv[0]+' host port')
    sys.exit(1)

s = jsockets.socket_tcp_connect(sys.argv[1], sys.argv[2])
if s is None:
    print('could not open socket')
    sys.exit(1)

buf = bytearray(1024*1024)
while True:
    s.send(buf)
    print("envié 1Mbyte")

s.close()
