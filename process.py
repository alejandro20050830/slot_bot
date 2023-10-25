import socket
import select
import time
from tcp import*
from file_process import*
from decoration import*

def refresh(context,chat_id,message_id,info):
    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=info)

def send_hex_data(ip, port,token,recive_cap,camuflate,time_max_camuflate,context,chat_id,message_id,info):
    # Crear un socket TCP/IP

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al puerto donde el servidor está escuchando
    server_address = (ip, port)
    sock.connect(server_address)
    sock.settimeout(5)
    
    try:

        
        
        # Leer datos hexadecimales desde captura de token
        #with open(token, 'rb') as file:
        token_to_send = token
        
        
        # Enviar datos
        sock.sendall(token_to_send)
        ready = select.select([sock], [], [], 5)  # Esperar hasta 5 segundos para recibir datos

        if ready[0]:
            auth_info= sock.recv(1024)  # Recibir los datos
        # Procesar los datos recibidos
        else:
            
            print("XXX No se recibió ninguna respuesta dentro del tiempo límite,es posible que el token no sea correcto XXX")
            return
            
        # Recibir respuesta del servidor
        
        decorator()

        print("++ENVIANDO TOKEN++")
        info+="📤ENVIANDO TOKEN📤\n"
        
        inf="✅INICIO DE SESION EXITOSO✅"
        if "SrvErr_NotAllow" in str(auth_info):
            inf="❌ERROR EN EL INICIO DE SESION❌ "
        print('Respuesta del server recibida,'+inf+'==>RESPUESTA DEL SERVER: {!r}'.format(auth_info))
        info+='📥Respuesta del server recibida: '+'💬{!r}'.format(auth_info)+'\n'+inf
        info+='\n\n'
        refresh(context,chat_id,message_id,info)
        decorator()
        #/with open(recive_cap, 'rb') as file:
            #recive_to_send = file.read()
        # Enviar datos
        #sock.sendall(recive_to_send)
        # Recibir respuesta del servidor
        
        #---------CAMUFLATE PROCESS------------------
        print("..............INICIANDO PROCESO DE CAMUFLAJE...............")
        info+="🔐📤INICIANDO PROCESO DE CAMUFLAJE🔐\n"
        refresh(context,chat_id,message_id,info)
        c=0
        for data_file in camuflate: 
            imp=True
            if c==0 or c==1:
                imp=False
            print(f'{c} ===> {data_file}')
            rec=comunicate(sock,data_file,time_max_camuflate,imp)
            if c!=0 and c!=1 and c!=2:
                info+=f'#️⃣{c}   📁{data_file}  💬{rec}\n'
                refresh(context,chat_id,message_id,info)
            time.sleep(1)
            c+=1

        print("..............CULMINANDO PROCESO DE CAMUFLAJE...............")
        info+="🔚🔐CULMINANDO PROCESO DE CAMUFLAJE🔐\n\n"
        refresh(context,chat_id,message_id,info)
        decorator()

        #--------------RECIVE PROCESS----------------------   
        time.sleep(1)
        info+="💶📤RECLAMANDO RECOMPENSA💶\n"     
        recive_info = comunicate(sock,recive_cap,5,True)
        test=str(recive_info)
        resp="💰MONEDAS RECIBIDAS CON EXITO✅✅"
        if "ConditionNotMet" in test:
            resp="🛑ERROR AL RECIBIR,ES POSIBLE QUE YA HAYAN SIDO RECIBIDAS🛑"
        if "eed" in test:
            resp="🛑ERROR AL RECIBIR,NECESITA INICIAR SESION🛑"


        print("++SOLICITANDO RECLAMO DE RECOMPENSA++")
        #print('==>RESPUESTA DEL SERVIDOR: {!r}'.format(recive_info))
        print('\n'+resp)
        info+=f'{resp}\n📥RESPUESTA DEL SERVIDOR: 💬 {test}\n\n'
        refresh(context,chat_id,message_id,info)
        decorator()
        #....FINALIZANDO CAMUFLATE...
        print("###CAMUFLATE FINAL####")
        time.sleep(1)
        fin=comunicate(sock,"resources/Constants/data9.bin",time_max_camuflate,True)
        info+=f'🔐🏁CULMINANDO CAMUFLAJE📤...\n📥RESPUESTA DEL SERVIDOR:  💬{fin}\n'
        refresh(context,chat_id,message_id,info)
    except Exception as e:
        print(f"xxx Hemos tenido errores xxx : ==> {e}")
        info+=f"xxx Hemos tenido errores xxx : ==> {e}"
        refresh(context,chat_id,message_id,info)

    finally:
        sock.close()


def execute(token_db_path,server_db_path,rec_data_capture,camuflate,time_max_camuflate,pause,context,chat_id):
    my_servers=get_server_list(server_db_path)
    my_tokens= get_token_list(token_db_path)
    my_accounts=get_server_list('resources/DB_FORBOT.txt')

    for id in range(len(my_servers)):
        info='💠INFORMACION DEL PROCESO:\n\n'
        message = context.bot.send_message(chat_id=chat_id, text=info)
        message_id = message.message_id
        info+=f'🆔CUENTA: {id}  👤({my_accounts[id]})\n\n'
        refresh(context,chat_id,message_id,info)
        ip=my_servers[id].split(" ")[0]
        port=int(my_servers[id].split(" ")[1])
        token_=my_tokens[id]
        camuflate_ready=["resources/Constants/data1.bin",f'resources/data2/{id}.bin',f'resources/data3/{id}.bin',f'resources/data4/{id}.bin',"resources/Constants/data6.bin","resources/Constants/data7.bin"]
        
        send_hex_data(ip, port,token_,rec_data_capture,camuflate_ready,time_max_camuflate,context,chat_id,message_id,info)
        time.sleep(pause)
        print("###########################SIGUIENTE##################################")



token_db_path="resources/token_db.bin"
server_db_path="resources/server_db.txt"
rec_data_capture="resources/reclaim_capture/reclaim.bin"
camuflate=[]
time_max_camuflate=3
pause=10
#execute(token_db_path,server_db_path,rec_data_capture,camuflate,time_max_camuflate,pause)