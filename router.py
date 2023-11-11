import sys
import socket
import aux

# tamaño del buffer
buff_size = 48

# ip del router
ip = sys.argv[1]
# puerto del router (simulando una IP)
port = int(sys.argv[2])
# nombre del archivo con la tabla de rutas
route_table = sys.argv[3]

# se crea un socketUDP
router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# se le hace bind a su dirección dada
router_socket.bind((ip, port))

# # ciclo while recibiendo de manera bloqueante
# while True:

# se obtiene un mensaje
mssg, address = router_socket.recvfrom(buff_size)

# se pasa a estructura
struct_mssg = aux.parse_packet(mssg)

# se consigue la ruta para llegar al destino
nxt_dir = aux.check_routes(route_table, (struct_mssg[0], struct_mssg[1]))

print(nxt_dir)




