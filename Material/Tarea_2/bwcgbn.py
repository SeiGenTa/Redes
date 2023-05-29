import sys, socket, jsockets, os, time
import random as rd
import threading
#global variables

MAX_TRIES = 100
HDR = 3
MAX_SEQ = 100

befSend = 0

def from_seq(c1,c2):
    return (c1-ord('0'))*10+(c2-ord('0'))

def to_char(num):
    if(num > 9999):
        print(f"to_char: bad num: {num}")
        return None

    return bytearray([ord('0')+num // 1000, ord('0')+num // 100%10, ord('0')+num // 10%10, ord('0')+num%10])

def to_num(c1,c2,c3,c4):
    return (c1-ord('0'))*1000+(c2-ord('0'))*100+(c3-ord('0'))*10+(c4-ord('0'))

def to_seq(num):
    if(num > 99):
        print(f"to_char: bad num: {num}");
        return None

    return bytearray([ord('0')+num // 10%10, ord('0')+num %10])

def creataSectionData(data,size:int) -> list():
    mydata = list()
    d = data.read(size)
    while d != b'':
        mydata.append(d)
        d = data.read(size)
        
    
    return mydata
    

def recv_loss(s:jsockets, size:int, loss:float) -> bytearray():
    try:
        while True:
            data = s.recv(size)
            if rd.random() * 100 <= loss:
                print("[recv_loss]")
            else:
                break
    except socket.timeout:
        data = None
        
    except socket.error:
        data = None
        
    return data

#this function return the status of send
def send_loss(s:jsockets, data:bytearray(), loss:float) -> str:
    if rd.random() * 100 > loss:
        s.send(data)
        return "successful"
    else:
        print("[send_loss]")
        return "failed"

def sendMult(s:jsockets, data:list(), loss:float,lastSucces:int,win_size:int) -> None:
    lenData = len(data)
    for i in range(win_size):
        if lastSucces + i < lenData:
            print(f'sending {lastSucces+i+1} data')
            info = b'D'+to_seq(lastSucces+i+1)+ data[lastSucces + i]
            send_loss(s, info, loss)
        else:
            break

#this call allows us to use main in other app.py for study
def main(size, timeout, loss, win_size, filein, host, port):
    s = jsockets.socket_udp_connect(host,port)
    if s is None:
        print('could not open socket')
        return "error_0"
        
    s.settimeout(TIMEOUT/100.0)
    
    try:
        print(filein)
        fdin = open(filein,"rb")
    except:
        print("error opening file")
        print(os.getcwd())
        return "error_1"
    
    tries = 0
    s.settimeout(TIMEOUT/1000.0)
    while tries < MAX_TRIES:
        sizeChar = to_char(size)
        pack = bytearray([ord('C'),ord('0'),ord('0')])+sizeChar
        send_loss(s, pack, loss)
        
        data = recv_loss(s, 7, loss)
        
        if data:
            if len(data) < 7 or data[0] != ord('A') or data[1] != ord('0') or data[2] != ord('0'):
                print('No recibí respuesta OK')
                sys.exit(1)
            else:
                break
        
        tries = tries + 1
        
    if tries == MAX_TRIES:
        print('No recibí respuesta OK')
        return "error_2"
        
    print(f'propuse paquete: {size}', file=sys.stderr)
    PACK_SIZE = to_num(data[3],data[4],data[5],data[6])
    print(f'recibo paquete: {size}', file=sys.stderr)

    s.settimeout(TIMEOUT/1000.0)
    
    _data = creataSectionData(fdin,PACK_SIZE)
    
    subDivSends = list(range(len(_data)))
    print(subDivSends)
    
    start = time.time()
    tries = 0
    
    befFirst = 0
    lenDatas = len(subDivSends)
    while tries < MAX_TRIES:
            #### CODIGO PARA CUANDO SE HAYA TERMINADO DE ENVIAR
        
        args = [s,_data,loss,befFirst,win_size]
        myThread = threading.Thread(target=sendMult,args=args)

        s.settimeout(TIMEOUT/1000.0)
        timeInit = time.time()
        myThread.start()
        for i in range(win_size):
            ack = recv_loss(s,3,loss)
            print(f'recibo ack: {ack}')
            if not ack or ack[0] != ord('A'): # Este ACK NO debe ser sólo Header
                print('fail in reception data')
                break
            
            try:
                removeValue = int(ack[1:])
                if befFirst < removeValue:
                    befFirst = removeValue
                    tries = -1
                
            except:
                pass

            timeRest = TIMEOUT/1000.0 - (timeInit - time.time())/1000.0
        
            if (timeRest) < 0.0: #si el tiempo de espera ya paso, se finaliza
                break
            s.settimeout(timeRest)    
        
        if befFirst >= lenDatas:
            print("se a enviado todo")
            break
        
        tries += 1 #si no hay cambios por 3 intentos se corta todo
        
    print(f'send E'+str(befFirst+1))
    tries = 0
    s.settimeout(TIMEOUT/1000.0)  
    while tries < MAX_TRIES:
        # Envío el EOF
        send_loss(s, b'E'+to_seq(lenDatas+1),loss)
        # Espero ACK de EOF que es raro
        ack = recv_loss(s, PACK_SIZE,loss)
        print(f'recibo eof ack: {ack}')
        
        if not ack or ack[0] != ord('A') or from_seq(ack[1],ack[2]) != lenDatas+1 or len(ack) == HDR: # Este ACK NO debe ser sólo Header
            tries=tries+1
            print('retry eof')
        else:
            break
        
        
    timeEnd = time.time()
    difTime = timeEnd - timeInit
    amountBytes = int(ack[3:])
    bw = amountBytes/difTime/1024/1024
    print(f"bytes enviados {amountBytes}, time: {difTime}, bw={bw} MBytes/s")
    
    return amountBytes, difTime, bw

if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' size timeout loss win_size filein host port')
    sys.exit(1)

SIZE = int(sys.argv[1])
TIMEOUT = int(sys.argv[2])
LOSS = int(sys.argv[3])
WINSIZE = int(sys.argv[4])
FILEIN = sys.argv[5]
HOST = sys.argv[6]
PORT = sys.argv[7]
main(SIZE, TIMEOUT, LOSS, WINSIZE, FILEIN, HOST, PORT)
