import socket
import sys
import threading
import lib.socketLibrary
import lib.encryptAES

from Crypto.Cipher import AES

# Decidimos la IP y el puerto del servidor
HOST = '127.0.0.1'  # La IP del servidor es la loca de la máquina
PORT = 5008  # El puerto tiene que ser superior a 1024, por debajo estan reservados
finished_message = b''

JOKE = b'Cual es el colmo de un programador? No poder programar sus vacaciones.'
BYE = 'bye'

def server_program():
    """ Ejecuta el programa Servidor """
    try:
        socket_escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket servidor creado')
    except socket.error:
        print('Fallo en la creación del socket servidor')
        sys.exit()

    try:
        # Definimosel punto de enlace del ervidor. El servidor está preparado en la IP 127.0.0.1 y puerto 5000
        socket_escucha.bind((HOST, PORT))
    except socket.error as e:
        print('Error socket: %s' % e)
        sys.exit()
        
    # El servidor puede escuchar hasta 5 clientes. En este ejmeplo sólo escuchará a 1 y se rompe la conexión
    socket_escucha.listen(5)

    while True:
        # El Servidor queda bloquedo en esta línea esperando a que un cliente se conecte a su IP y puerto
        # Si un cliente se conecta guardamos en conn del socket y en addr la información del cliente (IP y puerto del cliente)
        socket_atiende, addr_cliente = socket_escucha.accept()

        # Ejecución con Threads.
        lock = threading.Lock()
        t = threading.Thread(target=execute, args=(lock,socket_atiende,addr_cliente))
        t.start()


def execute(lock, socket_atiende, addr_cliente):
    """ Ejecuta la logica del programa """

    with lock:
        with socket_atiende:

            close = False

            while not close:
                print(f'[Server] Conexión exitosa con el cliente. {addr_cliente}')

                print ("[Server] Mensaje original: ", JOKE)
                message, key, iv = lib.encryptAES.generateKeys(JOKE)
                print("[Server] Mensaje Cifrado: ", message)

                # Send a Joke to Client and get message to client
                message = lib.socketLibrary.messageSendBinary(socket_atiende, message)

                # Send a Key to Client and get message to client
                message = lib.socketLibrary.messageSendBinary(socket_atiende, key)

                # Send an IV to Client and get message to client
                message = lib.socketLibrary.messageSendBinary(socket_atiende, iv)

                close = True


if __name__ == '__main__':
    server_program()
