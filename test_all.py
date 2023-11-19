import socket
import time

# dirección
ip = '127.0.0.1'
port = 9000

# socket UDP
test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# se le hace bind a su dirección dada
test_socket.bind((ip, port))

# rango de los puertos a hacer test
start = 8880
last = 8886

for i in range(start, last+1):
    for j in range(start, last+1):

        # se crea el mensaje
        mssg = ("{},{},hola, R{}!".format(ip, j, (j-8880))).encode()
        # se envía la mensaje al router
        test_socket.sendto(mssg, (ip, i))
        # se espera un poco para no colapsar la red
        time.sleep(1.5)

