import imp
import socket
import sys
import lib.socketLibrary
import lib.encryptAES

from Crypto.Cipher import AES
from setuptools import sic

HOST = '127.0.0.1'
PORT = 5008

CONTINUE = 'Si quieres cerrar la conexión escribe: [bye] ...: '
BYE = 'bye'

MESSAGE_TO_KEY = "Puedes mandarme la clave?"
MESSAGE_TO_IV = "Puedes mandarme el IV?"


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

            # Send message to Server to get a Key.
            key = lib.socketLibrary.messageRecieveBinary(socket_cliente, MESSAGE_TO_KEY)

            # Send message to Server to get an IV.
            iv = lib.socketLibrary.messageRecieveBinary(socket_cliente, MESSAGE_TO_IV)

            # desciframos usando la misma key e iv
            messageDecrypted = lib.encryptAES.decrypte(messageEncrypted, key, iv)
            print("[Cliente] Mensaje descifrado: ", messageDecrypted.decode("utf-8"))

            init_message = BYE


if __name__ == '__main__':
    client_program()
