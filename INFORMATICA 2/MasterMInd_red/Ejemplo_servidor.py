from socket import *
from Ejemplo_hilo import *


class ServerTCP:
    # constructor
    def __init__(self, host, port):  # variables clave y publicas
        self.serverHost = host
        self.serverPort = port
        self.ServerSocket = None

    def crearServer(self):
        self.ServerSocket = socket(AF_INET, SOCK_STREAM)
        self.ServerSocket.bind((self.serverHost, self.serverPort))
        self.ServerSocket.listen(1)
        print('El servidos esta listo para ser usado en el puerto: ', self.serverPort)

    def comunicacion(self):
        while True:
            clientsocket, direccion = self.ServerSocket.accept()
            print("conectado: ", direccion)
            hilo = socketHilo(clientsocket, direccion)
            hilo.start()


def main():
    localhost = "127.0.0.1"
    serverPort = 6001


    server = ServerTCP(localhost, serverPort)
    server.crearServer()
    server.comunicacion()


if __name__ == "__main__":
    main()
