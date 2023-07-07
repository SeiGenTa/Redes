from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import send
import sys


if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+'port-client host port-server')
    sys.exit(1)

# Dirección IP y puertos del cliente y servidor
cliente_ip = "2001:db8::1"
cliente_puerto = int(sys.argv[1])
servidor_ip = "2001:db8::1" #str(sys.argv[2])
servidor_puerto = int(sys.argv[3])

# Crear un paquete UDP personalizado con el mensaje de inyección
mensaje = "hackeado"
packet = IP( dst="localHost") / UDP(sport=cliente_puerto, dport=servidor_puerto) / mensaje

send(packet,count=100)
# Enviar el paquete al servidor
