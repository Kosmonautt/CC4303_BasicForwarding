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

# test de funcionalidad
IP_packet_v1 = "127.0.0.1,8881,hola, cómo estás?".encode()
parsed_IP_packet = parse_packet(IP_packet_v1)
IP_packet_v2_str = create_packet(parsed_IP_packet)
IP_packet_v2 = IP_packet_v2_str.encode()
print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))
