import json
from config import*

def get_token_list(token_db_path):
    lista = []
    with open(token_db_path, 'rb') as archivo:
        for linea in archivo:
            lista.append(linea.rstrip(b'\n'))  # Elimina la nueva línea al final de cada archivo
    return lista


def get_server_list(server_db_path):
    server_list = []
    with open(server_db_path, 'r') as archivo:
        for linea in archivo:
            # Elimina el caracter de nueva línea al final de cada línea
            linea = linea.rstrip('\n')
            server_list.append(linea)
        
    return server_list

def save_db(data):
    with open(db_path, 'w') as file:
        json.dump(data, file)

def read_db():   
    with open(db_path, 'r') as file:
        data = json.load(file)
    return data

def edit_db(key, new_value):
    global my_db
    data = read_db()
    data[key] = new_value
    save_db(data)
    my_db=read_db()

def save_bin(info,nombre_archivo_destino):
    with open(nombre_archivo_destino, 'wb') as archivo_destino:
        for lin in info:       
            archivo_destino.write(lin)
            archivo_destino.write(b'\n')  # Agrega una nueva línea entre cada archivo


def read_bin(nombre_archivo):
    lista = []
    with open(nombre_archivo, 'rb') as archivo:
        for linea in archivo:
            lista.append(linea.rstrip(b'\n'))  # Elimina la nueva línea al final de cada archivo
    return lista
def edit_bin(index,new_path,nombre_archivo_destino):
    actual_bin=read_bin(nombre_archivo_destino)
    actual_bin[index]=read_bin(new_path)[0]
    save_bin(actual_bin,nombre_archivo_destino)


#db_dates={'restante':0}
#save_db(db_dates)
#my_db=read_db()
#edit_db('restante',1)
#print(my_db['restante'])