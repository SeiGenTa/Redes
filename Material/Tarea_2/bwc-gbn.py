import socket, jsockets
import random as rd
import threading
#global variables

MAX_TRIES = 100
HDR = 3
MAX_SEQ = 100 

def creataSectionData(data:bytearray(),size:int) -> list():
    mydata = list()
    count = 1; lenData = len(data)
    while (count*size < lenData):
        subData = data[count*(size-1): count*(size) - 1]
        mydata.append(subData)
        count += 1
        
    subData = data[count*(size-1):]
    mydata.append(subData)
    
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
            send_loss(s, data[lastSucces + i], loss)
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
        fdin = open(filein,"rb")
    except:
        print("error opening file")
        return "error_1"
    
    tries = 0
    while tries < MAX_TRIES:
        sizeChar = to_char(size)
        sizeChar = (len(sizeChar) - 4)*0 + sizeChar
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
        
    print(f'propuse paquete: {PACK_SIZE}', file=sys.stderr)
    PACK_SIZE = to_num(data[3],data[4],data[5],data[6])
    print(f'recibo paquete: {PACK_SIZE}', file=sys.stderr)

    s.settimeout(TIMEOUT/1000.0)
    
    _data = creataSectionData(fdin.read(),PACK_SIZE)
    
    subDivSends = list(range(len(_data)))
    
    start = time.time()
    tries = 0
    while tries < MAX_TRIES:
        if subDivSends == []:
            print("se a enviado todo")
            return
            #### CODIGO PARA CUANDO SE HAYA TERMINADO DE ENVIAR
        befFirst = subDivSends[0]
        
        args = [s,_data,loss,befFirst,win_size]
        myThread = threading.Thread(target=sendMult,args=args)
        myThread.start()

        s.settimeout(TIMEOUT/1000.0)
        timeInit = time.time()
        for i in range(win_size):
            ack = recv_loss(s,PACK_SIZE,loss)
            print(f'recibo eof ack: {ack}')
            if not ack or ack[0] != ord('A'): # Este ACK NO debe ser sólo Header
                print('fail in reception data')
                break #ya que no llegaron los paquetes
            
            try:
                removeValue = int(ack[1:])
                subDivSends.remove(removeValue)
                
            except:
                pass
    
        if befFirst != subDivSends:
            tries = 0
        else:
            tries += 1
        
        timeRest = TIMEOUT/1000.0 - (timeInit - time.time())/1000.0
        
        if (timeRest) < 0.0: #si el tiempo de espera ya paso, se finaliza
            break
        s.settimeout(timeRest)    
        
    return

if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' size timeout loss win_size filein host port')
    sys.exit(1)

SIZE = int(sys.argv[1])
TIMEOUT = int(sys.argv[2])
LOSS = int(sys.argv[3])
WINSIZE = int(sys.argv[4])
FILEIN = open(sys.argv[5],"rb")
HOST = sys.argv[6]
PORT = sys.argv[7]
main(SIZE, TIMEOUT, LOSS, WINSIZE, FILEIN, HOST, PORT)
