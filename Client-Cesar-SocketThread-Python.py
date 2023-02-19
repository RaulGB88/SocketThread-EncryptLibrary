import imp
import socket
import sys
import lib.socketLibrary
import lib.encryptCesarASCI

from Crypto.Cipher import AES
from setuptools import sic

HOST = '127.0.0.1'
PORT = 5008

BYE = 'bye'
MESSAGE_TO_KEY = "Puedes mandarme la clave?"


def client_program():
    """ Ejecuta el programa Cliente """

    try:
        # 1- Creamos el Socket.
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket cliente creado')
    except socket.error:
        print('Fallo en la creación del socket cliente')
        sys.exit()

    # 2- Conectamos el Socket cliente al servidor
    socket_cliente.connect((HOST, PORT))

    execute(socket_cliente)


def execute(socket_cliente):
    """ Ejecuta la logica del programa """
    
    init_message = 'Conectado con el servidor' # El programa cliente escribe esto al servidor

    with socket_cliente:
        while init_message != BYE:
        
            # Recieve data: First message from server with encrypted message.
            messageEncrypted = socket_cliente.recv(1024)
            messageEncrypted = messageEncrypted.decode()

            # Send message to Server to get a Key.
            key = lib.socketLibrary.messagesText(socket_cliente, MESSAGE_TO_KEY)
            key = str(key).lower()

            # desciframos usando la misma key e iv
            messageDecrypted = lib.encryptCesarASCI.decrypt(messageEncrypted, key)
            print("[Cliente] Mensaje descifrado: ", messageDecrypted)

            init_message = BYE


if __name__ == '__main__':
    client_program()
