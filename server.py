import socket
import threading

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección IP del servidor (localhost)
PORT = 12345       # Puerto que utiliza el servidor

# Crear el socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lista para almacenar los clientes conectados
clients = []
nicknames = []

# Enviar mensajes a todos los clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)

# Manejar mensajes de un cliente específico
def handle(client):
    while True:
        try:
            # Recibir mensaje del cliente
            message = client.recv(1024)
            broadcast(message)
        except:
            # Eliminar y cerrar la conexión cuando hay un problema
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} se ha desconectado.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Recibir y manejar nuevas conexiones
def receive():
    while True:
        # Aceptar la conexión del cliente
        client, address = server.accept()
        print(f"Conectado con {str(address)}")

        # Solicitar y almacenar el apodo del cliente
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Informar a todos sobre la nueva conexión
        print(f'El apodo del cliente es {nickname}')
        broadcast(f'{nickname} se ha unido al chat!'.encode('utf-8'))
        client.send('Conectado al servidor!'.encode('utf-8'))

        # Iniciar el manejo de mensajes del cliente en un hilo separado
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Servidor en funcionamiento...')
receive()
