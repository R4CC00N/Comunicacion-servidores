# clase hija
from socket import *
import sys
import getopt
from MasterMind import *


class ClienteTCP:
    # constructor
    def __init__(self, name, ip, port):  # variables clave y publicas
        self.clientName = name
        self.serverIp = ip
        self.serverPort = port
        self.clientSocket = None  # usamos esto que ahora mismo no esta definido
        # debemos crear algo para crear el socket y para conectarlo

    def connet(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)  # lo convertimos en una variable de la clase
        self.clientSocket.connect((self.serverIp, self.serverPort))  # doble parentesis porque es la llamda y la tupla

    def send(self, mensaje):  # no ponemos el input pq no cumple lo que es una caja negra
        msg = self.clientName + " " + mensaje  # para mandar mi nombre con el mensaje
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
        while True:
            if self.clientSocket is None:
                self.connet()
            try:
                turn = input("Dame un numero de turnos: ")
            except ValueError:
                print("ERROR")
            mensaje = "TURNS#" + str(turn)
            self.send(mensaje)
            print(self.recibir())


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
    var.comunicacion


if __name__ == "__main__":
    main()
