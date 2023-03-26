#!/usr/bin/python3
# Echo client program
import jsockets
import sys

if len(sys.argv) != 3:
    print('Use: '+sys.argv[0]+' host port')
    sys.exit(1)

s = jsockets.socket_tcp_connect(sys.argv[1], sys.argv[2])
if s is None:
    print('could not open socket')
    sys.exit(1)

for line in sys.stdin:
    s.send(line.encode())
    data=s.recv(4096).decode()
    print(data, end = '')

s.close()
