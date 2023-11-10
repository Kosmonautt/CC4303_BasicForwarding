import sys
import socket

# tamaño del buffer
buff_size = 48

# ip del router
ip = sys.argv[1]
# puerto del router (simulando una IP)
port = sys.argv[2]
# nombre del archivo con la tabla de rutas
route_table = sys.argv[3]

# se abre el archivo con la tabla de rutas y se leen todas las líneas para guardarlo en una tabla
with open(route_table) as f:
    f_lines = f.readlines()

# se crea un socketUDP
router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# se le hace bind a su dirección dada
router_socket.bind((ip, port))

# # ciclo while recibiendo de manera bloqueante
# while True:
#     message, address = router_socket.recvfrom(buff_size)
#     print(message)



