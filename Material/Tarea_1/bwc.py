import jsockets
import sys
import time

if len(sys.argv) != 5:
    print('Use: '+sys.argv[0]+' size_file file host port')
    sys.exit(1)

host = sys.argv[3]
port = sys.argv[4]

#####Conectar servidor####
s = jsockets.socket_udp_connect(host, port)
if s is None:
    print('could not open socket')
    sys.exit(1)

size = sys.argv[1]
myFile = sys.argv[2]

def sendC(syze:int):
    s.settimeout(5)
    for i in range(5):
        time_init = time.time()
        s.send((f"C{syze}").encode())
        try:
            data = s.recv(12).decode()
            if (data[0] != "C") or (not data[1:].isdigit()):
                print("Respuesta no esperada")
                return 0 #Respuesta no esperada
            return data[1:].encode()
        except:
            print(f"intento: {i+1}")
        
    print("no hubo respuesta")
    return 0 #El 0 indicara que el server no respondio a nuestra peticion
        
    
def sendE(syze):
    s.settimeout(5)
    for i in range(5):
        time_init = time.time()
        s.send((f"C{syze}").encode())
        try:
            data = s.recv(12).decode()
            if (data[0] != "E") or (not data[1:].isdigit()):
                print("Respuesta no esperada")
                return 0 #Respuesta no esperada
            return data[1:].encode()
        except:
            print(f"intento: {i+1}")
        
    print("no hubo respuesta")
    return 0 #El 0 indicara que el server no respondio a nuestra peticion

def sendD(new_size):
    mysFile = open(myFile,"rb")
    info = mysFile.read()
    length_inf = info.__len__()
    mul = 0
    new_size -=1 ##cosiderando que D quita un byte
    while(new_size * (mul+1) < length_inf):
        s.send(f"D{(info[ new_size * mul : new_size * (mul + 1) - 1])}".encode())
        mul += 1
    s.send(info[ new_size * mul :])
    mysFile.close()
    return length_inf ##Retornamos el largo de la informacion

def main():
    print(f"se propuso un tamaño de: {size}")
    respC = sendC(size)
    if respC == 0:
        print("el servidor respondio de maneria no esperada o simplemente no respondio")
        sys.exit(1)
    print(f"El servidor respondio con: {respC.decode()}")
    
    cantBytes = int(respC)
    
    byteT = sendD(cantBytes) #Ya se sabemos sendD nos retorna la cantidad de bytes que se enviaron
    
    cantReciv = sendE(cantBytes)
    print(f"se envio: {byteT}, y se recibio: {cantReciv.decode()}")
    
    
main()
    
    