import time
from socket import *
from newSocket import *

class TCPClient():

    def __init__(self, host, port, name, frase):
        self.host = host
        self.port = port
        self.nombre = name
        self.frase = frase
        self.__socket = None

    def connect(self):
        self.__socket = newSocket(socket(AF_INET, SOCK_STREAM))
        self.__socket.connect((self.host, self.port))

    def disconnectSocket(self):
        self.__socket.close()
        self.__socket = None

    def senData(self, data):
        self.__socket.send(data.encode())

    def readData(self):
        msg = self.__socket.recv(1024).decode()
        return msg

    def communication(self):

        Fin = False

        self.senData("HELLO#"+self.nombre)

        while not Fin:
            self.senData(self.frase)

            time.sleep(3)
