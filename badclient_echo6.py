#!/usr/bin/python3
# Bad Echo client program
# Escribe 1 Mb al servidor y nunca escucha de vuelta
import jsockets
import sys
import threading

# lee desde el socket cada vez que le damos enter
def Rdr(s):
    for line in sys.stdin:
        try:
            data=s.recv(1024*1024).decode()
        except:
            data = None
        if not data:
            break
        lm = len(data)/1024/1024
        print(f'recvd: {lm} Mbytes')


if len(sys.argv) != 3:
    print('Use: '+sys.argv[0]+' host port')
    sys.exit(1)

s = jsockets.socket_tcp_connect(sys.argv[1], sys.argv[2])
if s is None:
    print('could not open socket')
    sys.exit(1)

# Creo thread que lee desde el socket hacia stdout:
newthread = threading.Thread(target=Rdr, args=(s,))
newthread.start()

buf = bytearray(1024*1024)
while True:
    s.send(buf)
    print("envié 1Mbyte")

s.close()
