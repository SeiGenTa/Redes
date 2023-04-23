import jsockets
import sys
import time
import pathlib
import os

if len(sys.argv) != 5:
    print('Use: '+sys.argv[0]+' size_chunks file host port')
    sys.exit(1)

host = sys.argv[3]
port = sys.argv[4]

#####Conectar servidor####
s = jsockets.socket_udp_connect(host, port) #UDP
if s is None:
    print("couldn't open socket")
    sys.exit(1)

size = sys.argv[1]
myFile = sys.argv[2]

def sendC(syze:int):
    s.settimeout(10)
    while len(syze) < 4:
        syze = "0" + str(syze) #ajustamos el tamaño de nuestro str a 4 (Cxxxx)
    for i in range(5):
        try:
            s.send(bytearray(f'C{syze}','utf-8')) #enviamos el tamaño propuesto
            data = s.recv(5).decode()  #como la respuesta es de la forma Cyyyy, como maximo mide 5 bytes (en 'utf-8')
            if (data[0] != "C") or (not data[1:].isdigit()):
                return 0 #Respuesta no esperada
            return data[1:]
        except:
            pass
        
    print("no hubo respuesta")
    return 0 #El 0 indicara que el server no respondio a nuestra peticion
        
    
def sendE(syze):
    for i in range(5):
        try:
            s.send(bytearray('E','utf-8'))
            data = s.recv(1024*1024).decode() #esperamos respuesta
            if (data[0] != "E") or (not data[1:].isdigit()):
                return 0
            return data[1:] #si data == "Ezzzz"... significa que ya esta bien y retornamos lo importante (zzzz)
        except:
            pass #re intentamos
        
    return 0 #El 0 indicara que el server no respondio a nuestra peticion

def sendD(new_size,direccion = myFile,raiz = "./"):
    ruta_archivo = os.path.join(raiz, direccion)
    if os.path.isfile(ruta_archivo):# Entrara en este if si la direccion es un archivo como una imagen
        # Si el archivo es un archivo, enviar su contenido a través del socket
        
        f = open(ruta_archivo, "rb") #abrimos el archivo
        info = f.read()
        length_inf = info.__len__() #obtenemos su tamaño
        #Sub dividimos al archivos en paquetes para el envio
        for i in range(0, len(info), (new_size)):
            #agregamos la D a cada uno de los paquetes
            paquete = bytearray("D","utf-8") + info[i:i+(new_size)]
            s.send(paquete)
                
        return length_inf
    
    #que llegue aqui significa que es una carpeta
    mysFile = os.listdir(ruta_archivo) #en listamos 
    length_inf_total = 0
    for archivo in mysFile: #recorremos cada subdireccion para el envio (permite inclusive
        # mandar carpeta dentro de sub carpetas)
        length_inf_total += sendD(new_size,direccion=archivo,raiz=ruta_archivo)
    return length_inf_total #retornamos el tamaño total de todo lo enviado

def main():

    respC = sendC(size)
    if respC == 0:
        print("el servidor respondio de maneria no esperada o simplemente no respondio")
        sys.exit(1)
    
    print(f"se propuso un tamaño de: {size}")
    print(f"El servidor respondio con: {respC}")
    cantBytes = int(respC)
    
    #Aqui iniciamos a enviar la informacion asi que aqui iniciaremos el cronometro
    time_init = time.time()
    
    byteT = sendD(cantBytes) #Ya sabemos sendD nos retorna la cantidad de bytes que se enviaron
    
    time_end = time.time() #Terminamos el proceso de envio de informacion
    #en este punto ya se enviaron todos los envios y esperaremos a que el servidor retorne su respuesta a que termino 
    #el envio de archivos (envio E)
    cantReciv = sendE(cantBytes)
    if cantReciv == 0:
        print("hubo un problema al recibir las respuestas")
        try:
            arch = open(name,"x")
            arch.write(f"bytes;Tamaño en bytes;Recibido en bytes;tiempo tardado;bw \n")
        except:
            arch = open(name,"a")
        arch.write(f"size;NULO;NULO;NULO;NULO \n")
        arch.close()
        sys.exit(1)
    
    tiempo_tardo = time_end-time_init
    bw = (int(cantReciv)/tiempo_tardo)/(1024*1024)
    print(f"bytes enviados: {byteT}, bytes recibidos: {cantReciv}, tiempo:{tiempo_tardo}, bw={bw}")
    
    name = "data_mejora.csv"
    try:
        arch = open(name,"x")
        arch.write(f"bytes;Tamaño en bytes;Recibido en bytes;tiempo tardado;bw \n")
    except:
        arch = open(name,"a")
    
    datos = [size,byteT,cantReciv,str(tiempo_tardo),bw]
    arch.write(f"{datos[0]};{datos[1]};{datos[2]};{datos[3]};{datos[4]} \n")
    arch.close()
    
    return datos
    
main()
    
    