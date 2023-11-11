# función que recibe un paquete y lo parsea, retornando cada componente en una estrucutra
def parse_packet(IP_packet):
    # el separador a usar
    separator = ","

    # se le hace decode
    IP_packet = IP_packet.decode()
    # se divide por comas
    IP_packet = IP_packet.split(separator)
    
    # se guarda la dirección IP
    ip = IP_packet[0]
    # se guarda el puerto
    port = IP_packet[1]
    # el mensaje (quizá en forma de lista, osea con más de un elemento)
    mssg_list = IP_packet[2:len(IP_packet)]

    # el mensaje en forma de string
    mssg = ""

    # se recontruye el mensaje (si es necesario)
    for slice in mssg_list:
        # se agrega al mensaje final
        mssg += slice
        # si es que es el útlimo, no se agrega una coma, si no es el último, entonces se agrega
        if(slice == mssg_list[len(mssg_list)-1]):
            pass
        else:
            mssg += ","

    # se retorna la estrcutura
    return [ip, port, mssg]

# función que recibe una estrcutra y la transforma en un mensaje
def create_packet(parsed_IP_packet):
    # el separador a usar
    separator = ","

    # se obtiene cada parte del mensaje
    IP = parsed_IP_packet[0]
    port = parsed_IP_packet[1]
    mssg = parsed_IP_packet[2]

    # se retorna el mensaje final
    return IP+separator+port+separator+mssg

# # test de funcionalidad
# IP_packet_v1 = "127.0.0.1,8881,hola, cómo estás?".encode()
# parsed_IP_packet = parse_packet(IP_packet_v1)
# IP_packet_v2_str = create_packet(parsed_IP_packet)
# IP_packet_v2 = IP_packet_v2_str.encode()
# print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))

# función que recibe el nombre del archivo con la rutas y la dirección de destino, retorna el par
# con la dirección de hacia donde debe "saltar", si no encuntrea ninguno retorna none
def check_routes(routes_file_name, destination_address):
    # variable que almacenará las lineas de la tabla
    f_lines = None

    # se abre el archivo con la tabla de rutas
    with open(routes_file_name) as f:
        # se leen todas las líneas y se guardan en una lista
        f_lines = f.readlines()

    # se obtienen la dirección IP y puerto de destino
    ip_destination = destination_address[0]
    port_destination = int(destination_address[1])

    # variable que guardará el valor de retorno (dir del sgte salto)
    nxt_jump = None

    # se lee cada linea de la tabla
    for line in f_lines:
        # se divide la línea por componente
        line = line.split()
        
        # IP que reprsenta la red
        cidr = line[0]
        # rangos de los puertos
        inf_r = int(line[1])
        sup_r = int(line[2])

        # si se encuentra la línea
        if((ip_destination == cidr) and ((inf_r <= port_destination) and (port_destination <= sup_r))):
            # se actualiza nxt_jump
            nxt_jump = (line[3], line[4])
            # se sale del for
            break
        
    # se retorna la dirección
    return nxt_jump
