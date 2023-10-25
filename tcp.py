import socket
import select
def comunicate(sock,path,time_max,imp):
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_address = (ip, port)
    #sock.connect(server_address)
    while True:
        r = select.select([sock], [], [], 0)
        if r[0]:
            sock.recv(4096)
        else:
            break
    sock.settimeout(time_max)
    try:
        with open(path, 'rb') as file:
            data_to_send = file.read()

        sock.sendall(data_to_send)
        ready = select.select([sock], [], [], time_max)  # Esperar hasta 5 segundos para recibir datos

        if ready[0]:
            
            data_recived= sock.recv(4096)  # Recibir los datos
        # Procesar los datos recibidos
        else:  
            print("XXX No se recibió ninguna respuesta dentro del tiempo límite")
            return
        
        if imp:
            print('==>RESPUESTA DEL SERVIDOR: {!r}'.format(data_recived))
        return data_recived
    except Exception as e:
        print(f"xxx Hemos tenido errores xxx : ==> {e}")
        return f"xxx Hemos tenido errores xxx : ==> {e}"

