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

# ciclo while donde se reciben mensajes
while True:
    # se espera a obtener un mensaje
    mssg, address = router_socket.recvfrom(buff_size)
    # se pasa a estrcutura
    struct_mssg = aux.parse_packet(mssg)
    
    # se revisa si el mensaje es para este router, si no, se hace forwarding
    if(struct_mssg[0] == ip and struct_mssg[1] == port):
        # se imprime el mensaje (sin headers)
        print(struct_mssg[2])
    # si no, se debe hacer forwarding
    else:
        # se consigue la ruta para hacer forwarding
        nxt_dir = aux.check_routes(route_table, (struct_mssg[0], struct_mssg[1]))

        # si es None, se descarta, si no, se hace forwarding
        if(nxt_dir == None):
            print("No hay rutas hacia {} para paquete {}".format(struct_mssg[1], struct_mssg[0]))
        else:
            # se imprime el forwarding que se realiza
            print("redirigiendo paquete {} con destino final {} desde {} hacia {}".format(struct_mssg[0], struct_mssg[1], port, nxt_dir[1]))
            # se hace el forwarding            
            router_socket.sendto(mssg, nxt_dir)



