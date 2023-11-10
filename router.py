import sys

# ip del router
ip = sys.argv[1]
# puerto del router (simulando una IP)
port = sys.argv[2]
# nombre del archivo con la tabla de rutas
route_table = sys.argv[3]

# se abre el archivo con la tabla de rutas y se leen todas las líneas para guardarlo en una tabla
with open(route_table) as f:
    f_lines = f.readlines()
    
print("IP", ip)
print("Port", port)
print(f_lines)

