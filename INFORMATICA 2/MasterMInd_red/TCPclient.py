# clase hija
from socket import *
import sys
import getopt
from newSocket import *
import random


class ClienteTCP:
    coin = {}

    # constructor
    def __init__(self, name, ip, port):  # variables clave y publicas
        self.clientName = name
        self.serverIp = ip
        self.serverPort = port
        self.clientSocket = None  # usamos esto que ahora mismo no esta definido
        # debemos crear algo para crear el socket y para conectarlo

        self.coin["cara"] = 1
        self.coin["cruz"] = 2

    def parseMyplif(self, flip: str) -> str:
        flipcode = 0
        if flip.lower() == "cara":
            flipcode = self.coin[flip.lower()]
        elif flip.lower() == "cruz":
            flipcode = self.coin[flip.lower()]
        elif flip.lower() == "fin":
            flipcode = -1
        return str(flipcode)

    def connet(self):
        self.clientSocket = newSocket(socket(AF_INET, SOCK_STREAM))  # lo convertimos en una variable de la clase
        # OJO CON EL NEWSOCKET
        self.clientSocket.connect((self.serverIp, self.serverPort))  # doble parentesis porque es la llamda y la tupla

    def send(self, mensaje):  # no ponemos el input pq no cumple lo que es una caja negra
        msg = mensaje  # para mandar mi nombre con el mensaje
        # el mensaje debe ser la combinacion de colores
        self.clientSocket.send(msg.encode())

    def recibir(self):
        mensajeModificado = self.clientSocket.recv(1024)  # tamaño buffer
        msg = mensajeModificado.decode()
        text = msg
        return text

    def close(self):
        self.clientSocket.close()

    def comunicacion(self):  # aqui hace todos los calculos
        fin = False
        while not fin:
            if self.clientSocket is None:
                self.connet()

            msg = input("cara o cruz:  ")
            parsemsg = self.parseMyplif(msg)  # puede estas dentro del cliente la clase importada
            if parsemsg == "0":
                print("otra vez")
            else:
                self.send(parsemsg)
                resultado = self.recibir()
                print(resultado)
                if parsemsg == "-1":
                    exit(1)


def conseguir_argumentos():
    name = None
    ip = "127.0.0.1"
    port = 1234

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "n:i:p:", ["name=", "ip =", "port ="])
        if len(argv) < 3:
            print("Faltan valores")
            sys.exit()
    except:
        print("Error en los argumentos introduzca -i IP -p PUERTO")
        sys.exit()

    for opt, arg in opts:
        if opt in ['-i', '--ip']:
            ip = arg
        elif opt in ['-n', '--name']:
            name = arg
        elif opt in ['-p', '--port']:
            port = int(arg)

    return name, ip, port


def main():
    name, ip, serverPort = conseguir_argumentos()
    var = ClienteTCP(name, ip, serverPort)
    var.connet()
    var.comunicacion()
    var.close()
    exit(1)


if __name__ == "__main__":
    main()
