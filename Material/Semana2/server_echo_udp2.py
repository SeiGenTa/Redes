#!/usr/bin/python3
# Echo server UDP program - using threads and multiple "connected" sockets
# Usa REUSE_PORT. Ojo que si recibo una inundación de paquetes UDP, hay un momento frágil entre
# que recibí el primer paquete desde el cliente, hasta que genero el nuevo socket para hablar con él
# si recibo un paquete en ese intertanto, le llegará al socket principal. No sé cómo evitar eso, así que
# recomiendo que el cliente espere una respuesta del servidor antes de seguir enviando paquetes...
import os, signal
import sys, threading
import socket, jsockets
import struct

class ClientThread(threading.Thread):
    def __init__(self, addr, s, data):
        threading.Thread.__init__(self)
        self.sock = s
        self.data1 = data
        self.addr = addr
    def run(self):
        print('Cliente Conectado')

        conn.connect(self.addr)
        # timeout de 10s, para que muera sin tráfico
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack("LL", 10, 0))

        # Ahora este socket sólo recibirá paquetes de este único cliente
        data = self.data1   # primer paquete que recibió el main
        while True:
            self.sock.send(data)
            try:
                data = self.sock.recv(1024)
            except:
                data = None
            if not data: break
        self.sock.close()
        print('Cliente desconectado')
        # la última magia es que al matar este socket, el original
        # vuelve a recibir estos paquetes, así que si el cliente vuelve
        # más tarde, se creará otro thread para él y no se dará ni cuenta
        # (en este caso solamente, que no hay estado)

s = jsockets.socket_udp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    # Esta es la magia del REUSEPORT: espero un primer paquete
    data, addr = s.recvfrom(1024)
    if not data: break
    # Para este cliente, voy a crear otro socket en el mismo port
    conn = jsockets.socket_udp_bind(1818)
    if conn is None:
        print('could not open 2nd socket')
        sys.exit(1)
    # Voy a crear un thread para que se conecte con ese cliente en el nuevo
    # socket!
    newthread = ClientThread(addr, conn, data)
    newthread.start()
    # Y yo sigo esperando paquetes de OTROS clientes solamente
