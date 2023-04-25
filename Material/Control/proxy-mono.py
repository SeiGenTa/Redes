#!/usr/bin/python3
# proxy 
# Mono-cliente, versión simple con select
import select
import sys
import jsockets

# Este el servidor de un socket ya conectado
# y el cliente del verdadero servidor (host, portout)
def proxy(conn, host, portout):

    conn2 = jsockets.socket_tcp_connect(host, portout)
    if conn2 is None:
        print('conexión rechazada por '+host+', '+portout)
        sys.exit(1)

    inputs = [conn, conn2]

    while inputs:
        readable,writable,exceptional = select.select(inputs,[],inputs)
        for s in exceptional: # cerramos sockets con error
            print('Cliente con error')
            conn.close()
            conn2.close()
            return
        for s in readable: # sockets con datos para mi
            if s is conn:
                data = conn.recv(1024*1024)
                if not data: # EOF
                    conn.close()
                    conn2.close()
                    return
                conn2.send(data)
            if s is conn2:
                data = conn2.recv(1024*1024)
                if not data: # EOF
                    conn.close()
                    conn2.close()
                    return
                conn.send(data)

# Main:

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' port-in host port-out')
    sys.exit(1)

portin = sys.argv[1]
host = sys.argv[2]
portout = sys.argv[3]

s = jsockets.socket_tcp_bind(portin)
if s is None:
    print('bind falló')
    sys.exit(1)

while True:
    conn, addr = s.accept();
    print(f'Cliente conectado: {addr}')
    proxy(conn, host, portout)
    print('Cliente desconectado')
