import socket
import threading

# Configuración del cliente
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 12345       # Puerto que utiliza el servidor

# Solicitar el apodo del usuario
nickname = input("Elige tu apodo: ")

# Crear el socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Escuchar mensajes del servidor y mostrarlos
def receive():
    while True:
        try:
            # Recibir mensajes del servidor
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Cerrar la conexión cuando hay un error
            print("Ha ocurrido un error!")
            client.close()
            break

# Enviar mensajes al servidor
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Iniciar hilos para escuchar y enviar mensajes
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
