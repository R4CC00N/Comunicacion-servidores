from socket import *


class ClientTCP:

    def __init__(self, name, port):
        self.serverName = name
        self.serverPort = port
        self.clientSocket = None

    def add_connect(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))  # realiza la conexion caracteristica en TCP

    def send_message(self):
        while True:
            msg = input('Introduzca la frase en minusculas : ')
            self.clientSocket.send(msg.encode())
        # el "send" no necesita parametros por que ya he establecido una comunicacion

    def recive_message(self):
        mensajeModificado = self.clientSocket.recv(1024)
        print(" Mensaje desde el servidor : ", mensajeModificado.decode())
        return mensajeModificado.decode()

    def desconnect(self):
        self.clientSocket.close()


def main():
    serverName = '127.0.0.1'
    serverPort = 1200
    cliente = ClientTCP(serverName, serverPort)  # type: ignore
    cliente.add_connect()
    cliente.send_message()
    cliente.recive_message()
    cliente.desconnect()


if __name__ == "__main__":
    main()
