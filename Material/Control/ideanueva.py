#!/usr/bin/python3
# proxy 
# Usando procesos para multi-clientes y threads dentros de cada proxy
import os, signal
import sys
import jsockets
import threading

def childdeath(signum, frame):
    os.waitpid(-1, os.WNOHANG)

def copy_sock(conn1, conn2, data = None):
    if data:
        conn2.send(data)
    while True:
        try:
            data = conn1.recv(9000)
        except:
            data = None
        if not data: break
        conn2.send(data)
    conn2.close()
    print('lost')

# Este el servidor de un socket ya conectado
# y el cliente del verdadero servidor (host, portout)
def proxy(data, addr, conn, host, portout):

    try:
        conn.connect(addr)
    except:
        print("hubo un error")
        sys.exit(1)

    conn2 = jsockets.socket_udp_connect(host, portout)
    if conn2 is None:
        print('conexión rechazada por '+host+', '+portout)
        sys.exit(1)

    print('Cliente conectado')

# copy_sock() corre en ambos threads, uno de conn->conn2 y otro de conn2->conn
    newthread1 = threading.Thread(target=copy_sock, daemon=True, args=(conn,conn2,data)) # el flag daemon es para que muera si muere el otro 
    newthread1.start()
    copy_sock(conn2, conn)
    print('Cliente desconectado')


# Main    
if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' port-in host port-out')
    sys.exit(1)

portin = sys.argv[1]
host = sys.argv[2]
portout = sys.argv[3]

signal.signal(signal.SIGCHLD, childdeath)

s = jsockets.socket_udp_bind(portin)
if s is None:
    print('bind falló')
    sys.exit(1)

while True:
    data, addr = s.recvfrom(1024)
    pid = os.fork()
    if pid == 0: # Este es el hijo
        conn = jsockets.socket_udp_bind(portin)
        s.close() # Cierro el socket que no voy a usar
        proxy(data, addr,conn, host, portout)
        sys.exit(0)
    