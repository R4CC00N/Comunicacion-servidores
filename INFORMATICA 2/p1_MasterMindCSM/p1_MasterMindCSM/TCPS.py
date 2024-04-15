from socket import *
from MMSS import *
# import listaEnlazada as lista


class TCPServer():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__socket = None
        # self.__lista = lista.listaEnlazada()
        # self.idpartida = 0

    def connect(self):
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind((self.host, self.port))
        self.__socket.listen(1)

    def disconnect(self):
        self.__socket.close()
        self.__socket = None

    def getSocket(self):
        return self.__socket

    def communication(self):
        while True:
            cliente, direccion = self.__socket.accept()
            print("Conexión desde:", direccion)

            socketCliente = MMSS(cliente, direccion)
            socketCliente.start()
