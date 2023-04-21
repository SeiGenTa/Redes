import jsockets
import sys
import time
import pathlib
import os

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
    s.settimeout(10)
    while len(syze) < 4:
        syze = "0" + str(syze)
    for i in range(5):
        time_init = time.time()
        s.send((f"C{syze}").encode())
        try:
            data = s.recv(1024).decode()
            if (data[0] != "C") or (not data[1:].isdigit()):
                print("Respuesta no esperada")
                return 0 #Respuesta no esperada
            return data[1:].encode()
        except:
            print(f"intento: {i+1}")
        
    print("no hubo respuesta")
    return 0 #El 0 indicara que el server no respondio a nuestra peticion
        
    
def sendE(syze):
    s.settimeout(10)
    for i in range(5):
        time_init = time.time()
        s.send((f"E").encode())
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

def sendD(new_size,direccion = myFile,raiz = "./"):
    length_inf_total = 0
    ruta_archivo = os.path.join(raiz, direccion)
    if os.path.isfile(ruta_archivo):# Entrara en este if si la direccion es un archivo como una imagen
        # Si el archivo es un archivo, enviar su contenido a través del socket
        
        with open(ruta_archivo, "rb") as f:
            info = f.read()
            length_inf = info.__len__()
            length_inf_total += length_inf
            paquetes = []
            for i in range(0, len(info), (new_size-1)):
                paquete = bytearray("D","utf-8") + info[i:i+(new_size-1)]
                paquetes.append(paquete)
                

            for paquete in paquetes:
                # Agregamos la letra "D" al inicio del paquete
                # Aquí podríamos encriptar el paquete antes de enviarlo
                s.send(paquete)
        return length_inf_total
    
    #que llegue aqui significa que es una carpeta
    mysFile = os.listdir(ruta_archivo)
    for archivo in mysFile:
        length_inf_total += sendD(new_size,direccion=archivo,raiz=ruta_archivo)
    return length_inf_total

def main():
    print(f"se propuso un tamaño de: {size}")
    respC = sendC(size)
    if respC == 0:
        print("el servidor respondio de maneria no esperada o simplemente no respondio")
        sys.exit(1)
    print(f"El servidor respondio con: {respC.decode()}")
    cantBytes = int(respC)
    
    #Aqui iniciamos a enviar la informacion asi que aqui iniciaremos el cronometro
    time_init = time.time()
    
    byteT = sendD(cantBytes) #Ya se sabemos sendD nos retorna la cantidad de bytes que se enviaron
    
    #en este punto ya se enviaron todos los envios y esperaremos a que el servidor retorne su respuesta a que termino 
    #el envio de archivos (envio E)
    cantReciv = sendE(cantBytes)
    if cantReciv == 0:
        print("hubo en problema al recibir las respuestas")
        sys.exit(0)
    time_end = time.time()
    
    print(f"se envio: {byteT}, y se recibio: {cantReciv.decode()} ")
    print(f"tardo: {time_end-time_init} segundos")
    
    
main()
    
    