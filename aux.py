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
    return [ip, int(port), mssg]

# función que recibe una estrcutra y la transforma en un mensaje
def create_packet(parsed_IP_packet):
    # el separador a usar
    separator = ","

    # se obtiene cada parte del mensaje
    IP = parsed_IP_packet[0]
    port = str(parsed_IP_packet[1])
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
            nxt_jump = (line[3], int(line[4]))
            # se sale del for
            break
        
    # se retorna la dirección
    return nxt_jump

# clase que representa todas las posibles salidas del router para una dirección de destino específica, en el router actual
class Forward:
    def __init__(self, destination_address):
        self.destination_address = destination_address
        self.jumps = None
        self.i = None
        self.len = None

    # función que inicializa la lista con todas las posibles salidas
    def innit_jump_list(self, route_table):
        # la lista de saltos se inicializa como una lista vacía
        self.jumps = []

        # se obtienen la dirección IP y puerto de destino
        ip_destination = self.destination_address[0]
        port_destination = int(self.destination_address[1])

        # se lee cada linea de la tabla
        for line in route_table:
            # se divide la línea por componente
            line = line.split()
            
            # IP que reprsenta la red
            cidr = line[0]
            # rangos de los puertos
            inf_r = int(line[1])
            sup_r = int(line[2])

            # si se encuentra una línea que corresponde
            if((ip_destination == cidr) and ((inf_r <= port_destination) and (port_destination <= sup_r))):
                # se actualiza la lista con el par ip lista
                self.jumps.append((line[3], int(line[4])))
        
        # se inicializa el índice
        self.i = 0
        # se guarda el largo de la lista
        self.len = len(self.jumps)

    # función que retorna el siguiente valor de la lista cíclica y actualiza el índice
    def get_nxt_jump(self):
        # si es que la lista es de tamaño 0 (vacía, osea no hay saltos) se retorna none
        if (self.len == 0):
            return None
        
        # se consigue el elemento de la lista
        nxt_jump = self.jumps[self.i]
        # se actualiza el índice
        self.i = (self.i+1)%self.len
        # se retorna el siguiente salto
        return nxt_jump

# clase que representa todas las listas de salidas de el router para cada dirección de destino
class ForwardList:
    def __init__(self, current_address):
        self.current_address = current_address
        self.forward_list = []

    # función que agrega un objeto Forward a la lista
    def add_forward(self, new_forward):
        self.forward_list.append(new_forward)

    # función que dice si es que se encuentra el objeto 
    # asociado a la dirección de destino dada
    def in_forward_list(self, destination_address):
        # dice si está o no en la lista
        in_list = False

        # para cada obejto en la lista
        for forward in self.forward_list:
            # si la dirección de destino es correcta
            if(forward.destination_address == destination_address):
                # está en la lista
                in_list = True
        
        return in_list

    # función que recibe una dirección de destino (ip y puerto)
    # y retorna el par (ip, puerto) que le corresponde del round 
    # robin (puede ser None)
    def get_nxt_jump(self, destination_address):
        # para cada obejto en la lista
        for forward in self.forward_list:
            # si la dirección de destino es correcta
            if(forward.destination_address == destination_address):
                # se consigue el siguiente salto (y actualiza su indice)
                nxt_jump = forward.get_nxt_jump()
                # se retorna el valor
                return nxt_jump