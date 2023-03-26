# Echo client program
import jsockets
import sys

s = jsockets.socket_tcp_connect('localhost', 1818)
if s is None:
    print('could not open socket')
    sys.exit(1)

s.send(b'hola')
data = s.recv(1024)
s.close()
print('Received', repr(data))
