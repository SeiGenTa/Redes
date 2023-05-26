#!/usr/bin/python3
# bw server UDP program, ventana de recepción 1
# sirve para cliente S&W y GoBackN
import socket, jsockets
import sys, threading
import time
import struct
import tempfile

HDR = 3
MAX_SEQ = 100  # 0-99

def to_num(c1,c2,c3,c4):
    return (c1-ord('0'))*1000+(c2-ord('0'))*100+(c3-ord('0'))*10+(c4-ord('0'))

def to_char(num):
    if(num > 9999):
        print(f"to_char: bad num: {num}");
        return None

    return bytearray([ord('0')+num // 1000, ord('0')+num // 100%10, ord('0')+num // 10%10, ord('0')+num %10])

def from_seq(c1,c2):
    return (c1-ord('0'))*10+(c2-ord('0'))

def to_seq(num):
    if(num > 99):
        print(f"to_char: bad num: {num}");
        return None

    return bytearray([ord('0')+num // 10%10, ord('0')+num %10])

class ClientThread(threading.Thread):
    def __init__(self, addr, s, data):
        threading.Thread.__init__(self)
        self.sock = s
        self.data1 = data
        self.addr = addr
    def run(self):
        print('Cliente Conectado')

        PACK_SIZE = 9000
        TIMEOUT = 10 # s
        conn = self.sock
        conn.connect(self.addr)
        # timeout de 10s, para que muera sin tráfico
        conn.settimeout(TIMEOUT) # 10 s

        # Ahora este socket sólo recibirá paquetes de este único cliente
        data = self.data1   # primer paquete que recibió el main

        if len(data) < 7 or data[0] != ord('C') or data[1] != ord('0') or data[2] != ord('0'):
            print(f'Rechazo conexión, error de protocolo: {data}')
            return

        sz = to_num(data[3],data[4],data[5],data[6])
        print(f'recibo pack={sz}')
        if sz > PACK_SIZE or sz <= 0:
            sz = PACK_SIZE

        print(f'usando sz={sz}')

        pack = bytearray([ord('A'),ord('0'),ord('0')])+to_char(sz)
        conn.send(pack)

        # Recibo archivo completo
        cnt = 1
        tbytes = 0
        eof = False
        while True:
            # Recibo paquete
            try:
                data = conn.recv(sz+HDR) # OJO: tamaño acordado es sin header
            except:
                data = None
            if not data:
                if not eof:
                    print('falla recepción')
                    conn.close()
                    return
                else:
                    break

            if len(data) < HDR or (data[0] != ord('D') and data[0] != ord('E')): # Esto es un error, no entendí
                continue

            # Ver si es el paquete esperado
            if from_seq(data[1],data[2]) == cnt:
                print(f'Recibi: {data[0:HDR]}')
                if data[0] == ord('E'):   # EOF
                    # Envio ACK del EOF
                    conn.send(b'A'+bytes([data[1],data[2]])+str(tbytes).encode('UTF-8'))
                    print(f'Envío: eof-ack, {cnt}, {str(tbytes)}')
                    eof = True
                elif data[0] == ord('D'):
                    # Envio ACK
                    conn.send(b'A'+bytes([data[1],data[2]]))
                    print(f'Envío: ack, {cnt}')
                    tbytes = tbytes + len(data) - HDR
                    cnt = (cnt+1) % MAX_SEQ
            else:
                print(f'Recibi paquete malo: {from_seq(data[1],data[2])} expecting: {cnt}')
                # Siempre envío ACK antiguo igual
                conn.send(b'A'+to_seq(((cnt-1)+MAX_SEQ)%MAX_SEQ))
                print(f'Envio ACK antiguo: {((cnt-1)+MAX_SEQ)%MAX_SEQ}')

        print(f'Recibi EOF con {tbytes} bytes')

        conn.close()
        print('Cliente desconectado')
        # la última magia es que al matar este socket, el original
        # vuelve a recibir estos paquetes, así que si el cliente vuelve
        # más tarde, se creará otro thread para él y no se dará ni cuenta
        # (en este caso solamente, que no hay estado)


s = jsockets.socket_udp_bind(1819)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    # Esta es la magia del REUSEPORT: espero un primer paquete
    data, addr = s.recvfrom(1024)
    if not data or data[0] != ord('C'):
        continue
    # Para este cliente, voy a crear otro socket en el mismo port
    conn = jsockets.socket_udp_bind(1819)
    if conn is None:
        print('could not open 2nd socket')
        sys.exit(1)
    # Voy a crear un thread para que se conecte con ese cliente en el nuevo
    # socket!
    newthread = ClientThread(addr, conn, data)
    newthread.start()
    # Y yo sigo esperando paquetes de OTROS clientes solamente
