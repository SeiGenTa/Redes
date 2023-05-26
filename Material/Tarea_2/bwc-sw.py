#!/usr/bin/python3
# bwc client UDP program
# Envía un archivo al servidor en UDP y recibe de vuelta: OK-bytes recibidos.
# Protocolo Stop-and-Wait con el servidor, modificarlo a Go-Back-N
import socket, jsockets
import sys, threading
import time
import struct, random

global PACK_SIZE, TIMEOUT
global loss_rate

MAX_TRIES = 100
HDR = 3
MAX_SEQ = 100   # seqn entre 0-99

def to_num(c1,c2,c3,c4):
    return (c1-ord('0'))*1000+(c2-ord('0'))*100+(c3-ord('0'))*10+(c4-ord('0'))

def to_char(num):
    if(num > 9999):
        print(f"to_char: bad num: {num}")
        return None

    return bytearray([ord('0')+num // 1000, ord('0')+num // 100%10, ord('0')+num // 10%10, ord('0')+num%10])

def from_seq(c1,c2):
    return (c1-ord('0'))*10+(c2-ord('0'))

def to_seq(num):
    if(num > 99):
        print(f"to_char: bad num: {num}");
        return None

    return bytearray([ord('0')+num // 10%10, ord('0')+num %10])

# Envía un paquete con loss_rate porcentaje de pérdida
def send_loss(s, data):
    global loss_rate

    if random.random() * 100 > loss_rate:
        s.send(data)
    else:
        print("[send_loss]")

# Recibe un paquete con loss_rate porcentaje de pérdida
# Si decide perderlo, vuelve al recv y no retorna aun
# Retorna None si hay timeout o error
def recv_loss(s, size):
    global loss_rate

    try:
        while True:
            data = s.recv(size)
            if random.random() * 100 <= loss_rate:
                print("[recv_loss]")
            else:
                break
    except socket.timeout:
        # print('timeout', file=sys.stderr)
        data = None
    except socket.error:
        # print('recv err', file=sys.stderr)
        data = None

    return data

# Main
if len(sys.argv) != 7:
    print('Use: '+sys.argv[0]+' size timeout loss filein host port')
    sys.exit(1)

PACK_SIZE = int(sys.argv[1])
TIMEOUT = int(sys.argv[2])
loss_rate = int(sys.argv[3])
fdin = open(sys.argv[4], "rb")

s = jsockets.socket_udp_connect(sys.argv[5], sys.argv[6])
if s is None:
    print('could not open socket')
    sys.exit(1)

s.settimeout(TIMEOUT/100.0) # para conexión: 10*TIMEOUT

tries = 0
while tries < MAX_TRIES:
    # Anuncio Conexión
    pack = bytearray([ord('C'),ord('0'),ord('0')])+to_char(PACK_SIZE)
    send_loss(s, pack)

    data = recv_loss(s, PACK_SIZE)

    if data:
        if len(data) < 7 or data[0] != ord('A') or data[1] != ord('0') or data[2] != ord('0'):
            print('No recibí respuesta OK')
            sys.exit(1)
        else:
            break

    tries = tries + 1

if tries == MAX_TRIES:
    print('No recibí respuesta OK')
    sys.exit(1)

print(f'propuse paquete: {PACK_SIZE}', file=sys.stderr)
PACK_SIZE = to_num(data[3],data[4],data[5],data[6])
print(f'recibo paquete: {PACK_SIZE}', file=sys.stderr)

s.settimeout(TIMEOUT/1000.0)
cnt = 1
start = time.time()
# Envío archivo completo
while True:
    # Leo un paquete
    data = fdin.read(PACK_SIZE)
    if data == b'':
        break
    tries = 0
    while tries < MAX_TRIES:
        # Lo envío
        print(f'sending: {cnt} data')
        send_loss(s, b'D'+to_seq(cnt)+data)
        # espero el ACK
        ack = recv_loss(s, PACK_SIZE)
        if not ack or ack[0] != ord('A') or from_seq(ack[1],ack[2]) != cnt: # incluye timeout
            print('falla ack')
        else:
            print(f'Recibo ACK: {cnt}')
            cnt = (cnt+1) % MAX_SEQ
            break
        tries = tries+1

    if tries >= MAX_TRIES:
        print('too many tries')
        sys.exit(1)

# EOF
print(f'send EOF, seq={cnt}')
tries = 0
while tries < MAX_TRIES:
    # Envío el EOF
    send_loss(s, b'E'+to_seq(cnt))
    # Espero ACK de EOF que es raro
    ack = recv_loss(s, PACK_SIZE)
    print(f'recibo eof ack: {ack}')
    if not ack or ack[0] != ord('A') or from_seq(ack[1],ack[2]) != cnt or len(ack) == HDR: # Este ACK NO debe ser sólo Header
        tries=tries+1
        print('retry eof')
    else:
        break

if tries >= MAX_TRIES:
    print('3: No recibí respuesta del servidor')
    sys.exit(1)

# Extraigo número de bytes recibidos en el servidor
ack = bytearray(ack)
del ack[0:HDR]
r_bytes = int(ack.decode())

# Medición ancho de banda final
ti = time.time()-start
s.close()
fdin.close()
bw = r_bytes/ti/1024/1024
print(f'bytes enviados={r_bytes}, time={ti}, bw={bw} MBytes/s')
