from process import*
from config import*
from telegram import Bot
import threading
from datetime import datetime
import pytz
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
my_db=read_db()


active=True

BOT_TOKEN='5187106848:AAHCZUlrUNhEva-IbGrlQpmR9z60_1b_O5I'
# Configura el registro para ver los mensajes de error

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def show_db(update,context):
    token=get_token_list(token_db_path)
    server=get_server_list(server_db_path)
    users=get_server_list('resources/DB_FORBOT.txt')
    info="DATA ACTUAL\n\n"
    for id in range(len(token)):

        info+=f'{id} {users[id]} SERVER: {server[id]}\nToken: {token[id]} '
        info+='\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=info)

def edit_token(update,context):
    full_text = update.message.text

    # Verificar si hay un espacio en el mensaje
    if ' ' in full_text:
        # Obtener el texto después del comando y el espacio
        index = int(full_text.split(' ', 1)[1])
    else:
        index = ''
    print(index)
    if update.message.reply_to_message.document:

        desactivate(update,context)
        file_id = update.message.reply_to_message.document.file_id
        file_name = update.message.reply_to_message.document.file_name
        # Descarga el archivo
        new_file = context.bot.get_file(file_id)
        new_file.download("resources/edittoken.bin")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Archivo descargado: {file_name}\nHEMOS DESCARGADO EL ARCHIVO\n")
        time.sleep(2)
        antiguo=read_bin(token_db_path)
        edit_bin(index,"resources/edittoken.bin",token_db_path)
        actual=read_bin(token_db_path)
        my_accounts=get_server_list('resources/DB_FORBOT.txt')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"HEMOS ACTUALIZADO EL NUEVO VALOR EN LA DATABASE PARA EL USUARIO {my_accounts[index]}\nAntiguo: {antiguo[index]}\n Actual: {actual[index]}")
        if os.path.exists("resources/edittoken.bin"):
            os.remove("resources/edittoken.bin")
            print("Archivo eliminado exitosamente.")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"HEMOS ELIMINADO EL ARCHIVO BASURA CONTENEDOR DEL TOKEN\n")
        else:
            print("El archivo no existe.")
        
        activate(update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, responde a un archivo que contenga la databse de tokens")



def activate(update, context):
    global active
    active = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="El proceso ha sido activado")


# Define la función para el comando /desactivar
def desactivate(update, context):
    global active
    active = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="El proceso ha sido desactivado")

def run_process(context, chat_id):
    
    zona_horaria_cuba = pytz.timezone('America/Havana')

    # Obtener la fecha y hora actual en Cuba
    fecha_hora_actual = datetime.now(tz=zona_horaria_cuba)

    # Formatear la fecha y hora
    formato_fecha_hora = '%Y-%m-%d %H:%M:%S %Z%z'
    fecha_hora_formateada = fecha_hora_actual.strftime(formato_fecha_hora)

    
    
  

    while True:
        my_db=read_db()
        if active:
            
            
            if time.time()-my_db['HI']>3840:
                message =context.bot.send_message(chat_id=chat_id, text=f'💵💎Iniciando proceso....\n🕣Fecha de inicio : {fecha_hora_formateada}')
                hora_inicial = time.time()
                edit_db('HI',hora_inicial)
                print("ejecuting...")       
                execute(token_db_path,server_db_path,rec_data_capture,camuflate,time_max_camuflate,pause,context,chat_id)#Ejecutar el pseudocódigo o función del otro proceso
                
                hora_actual = time.time()
                edit_db('HF',hora_actual)
                calculate_duration=time.time()-hora_inicial
                context.bot.send_message(chat_id=chat_id, text=f'🟢EL PROCESO HA CULMINADO🟢\n🕣Duracion : {round(calculate_duration,2)} segundos\n💨Fecha de comienzo: {fecha_hora_formateada}\n🏁Fecha de culminacion: {datetime.now(tz=zona_horaria_cuba).strftime(formato_fecha_hora)}')
                barra=''
                percent=5
                message1 = context.bot.send_message(chat_id=chat_id, text="🕣INICIANDO BARRA DE PROGRESO")
                message_id = message1.message_id
                while hora_actual - hora_inicial < 3840:
                    progress = (hora_actual - hora_inicial) / 3840
                    if progress*100>percent:
                        barra+='🟥'
                        percent+=5
                        
                    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'💠Progreso: {round(progress * 100,2)}%\n 🕣Restante: {3840-(round(hora_actual-hora_inicial,2))} segundos \n[{barra}')
                    time.sleep(1)
                    
                    
                    hora_actual = time.time()
                    edit_db('HF',hora_actual)

                    if not active:
                        break
                
                
            else:
                barra=''
                percent=5
                hora_inicial = my_db['HI']
                hora_actual = time.time()
                message1 = context.bot.send_message(chat_id=chat_id, text="🕣INICIANDO BARRA DE PROGRESO")
                message_id = message1.message_id
                while hora_actual-hora_inicial<3840:
                    
                    progress = (hora_actual - hora_inicial) / 3840
                    if progress*100>percent:
                        con=progress*100  
                        while con>0:
                            con-=percent
                            barra+='🟥'
                            
                        percent+=5
                        
                    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'💠Progreso: {round(progress * 100,2)}%\n 🕣Restante: {3840-(round(hora_actual-hora_inicial,2))} segundos \n[{barra}')
                    time.sleep(1)
                    
                    hora_actual = time.time()
                    edit_db('HF',hora_actual)

                    if not active:
                        break

           
        else:

            # Esperar un tiempo antes de verificar nuevamente si se reactiva el proceso
            print("desactivate..")
            time.sleep(3)
            
def run_process1(context):
    while True:
        if active:
            hora_inicial = time.time()
            
            print("ejecuting...")       
            #execute(token_db_path,server_db_path,rec_data_capture,camuflate,time_max_camuflate,pause)  # Ejecutar el pseudocódigo o función del otro proceso
            hora_actual = time.time()
            while hora_actual - hora_inicial <3840:

                time.sleep(60)

        else:
            # Esperar un tiempo antes de verificar nuevamente si se reactiva el proceso
            print("desactivate..")
            time.sleep(1)

# Define la función para el comando /start

def start(update, context):
    bot = update.effective_message.bot
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="¡Hola! Bienvenido")
    if activate:
        thread = threading.Thread(target=run_process, args=(context, chat_id))
        thread.start()
    else:
        context.bot.send_message(chat_id=chat_id, text="POR FAVOR PRIMERO ACTIVA EL BOT CON EL COMANDO /activate")
    #thread.join()
# Define la función para el comando /download
def down_server_db(update, context):
    # Verifica que se haya respondido a un archivo
    if update.message.reply_to_message.document:
        desactivate(update,context)
        file_id = update.message.reply_to_message.document.file_id
        file_name = update.message.reply_to_message.document.file_name
        # Descarga el archivo
        new_file = context.bot.get_file(file_id)
        new_file.download("resources/server_db.txt")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Archivo descargado: {file_name}\nLA DATABASE DE LOS SERVERS HA SIDO ACTUALIZADA")
        activate(update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, responde a un archivo que contenga la database de servers")

def down_token_db(update, context):
    # Verifica que se haya respondido a un archivo
    if update.message.reply_to_message.document:
        desactivate(update,context)
        file_id = update.message.reply_to_message.document.file_id
        file_name = update.message.reply_to_message.document.file_name
        # Descarga el archivo
        new_file = context.bot.get_file(file_id)
        new_file.download("resources/token_db.bin")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Archivo descargado: {file_name}\nLA DATABASE DE LOS TOKENS HA SIDO ACTUALIZADA")
        activate(update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, responde a un archivo que contenga la databse de tokens")

# Define la función para manejar mensajes
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor,ejecute el comando correcto")

def main():
    # Crea un objeto Updater y pasa el token de tu bot de Telegram
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Obtiene el despachador para registrar los controladores
    dispatcher = updater.dispatcher

    # Registra los controladores de comandos y mensajes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("edit_token", edit_token))
    dispatcher.add_handler(CommandHandler("show_db", show_db))
    dispatcher.add_handler(CommandHandler("server_update", down_server_db))
    dispatcher.add_handler(CommandHandler("token_update", down_token_db))
    dispatcher.add_handler(CommandHandler("activate", activate))
    dispatcher.add_handler(CommandHandler("desactivate", desactivate))
    dispatcher.add_handler(MessageHandler(Filters.reply,down_server_db))
    dispatcher.add_handler(MessageHandler(Filters.reply,down_token_db)) 
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Inicia el bot
    updater.start_polling()
    #thread = threading.Thread(target=run_process, args=(dispatcher.bot,))
    #thread.start()
    # Detiene el bot en caso de presionar Ctrl + C
    #thread.join()
    updater.idle()
    

if __name__ == '__main__':
    main()