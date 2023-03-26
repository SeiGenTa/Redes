#!/usr/bin/python3
# Echo server program - version of server_echo.c
import jsockets

s = jsockets.socket_tcp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept();
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
    conn.close()
    print('Client disconnected')
