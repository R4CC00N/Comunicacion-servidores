# clase hija
from socket import *
import sys
import getopt
from MasterMind import *


class ClienteTCP:
    # constructor
    def __init__(self, ip, port):  # variables clave y publicas
        self.serverIp = ip
        self.serverPort = port
        self.clientSocket = None  # usamos esto que ahora mismo no esta definido
        # debemos crear algo para crear el socket y para conectarlo

    def connet(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)  # lo convertimos en una variable de la clase
        self.clientSocket.connect((self.serverIp, self.serverPort))  # doble parentesis porque es la llamda y la tupla

    def send(self, mensaje):  # no ponemos el input pq no cumple lo que es una caja negra
        msg = mensaje  # para mandar mi nombre con el mensaje
        # el mensaje debe ser la combinacion de colores
        self.clientSocket.send(msg.encode())

    def recibir(self):
        mensajeModificado = self.clientSocket.recv(1024)  # tamaño buffer
        msg = mensajeModificado.decode()
        print("Mensaje desde el servidor : ", msg)
        return msg

    def close(self):
        self.clientSocket.close()

    def comunicacion(self):  # aqui hace todos los calculos
        """
        SI QUIERES MODIFICAR COSAS ES AQUI O EN UNA FUNCION DE LA CLASE NUEVA
        ADEMAS SI QUIERES PUEDES PONER MAS FORMAS DE MANDAR UN MENSAJE
        TE FALTA EL SECRET CODE Y SI QUIERES OTRO MENSAJE PARA CERRAR EL JUEGO
        """
        game = False
        while not game:
            if self.clientSocket is None:
                self.connet()
            try:
                turn = input("Dame un numero de turnos: ")
            except ValueError:
                print("ERROR")
            mensaje = "TURNS#" + str(turn)
            self.send(mensaje)
            resultado = self.recibir()
            codigo = resultado.split("#")
            if codigo[0].lower() == "turns":
                game = True
                print(resultado)
        while game:
            if self.clientSocket is None:
                self.connet()
            try:
                turn = input("Dame la jugaga: ")
            except ValueError:
                print("ERROR")
            mensaje = "COLORES#" + turn
            self.send(mensaje)
            resultado = self.recibir()
            print(resultado)



def main():
    ip = "127.0.0.1"
    serverPort = 6001

    var = ClienteTCP(ip, serverPort)
    var.connet()
    var.comunicacion()


if __name__ == "__main__":
    main()
