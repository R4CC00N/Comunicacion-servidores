# clase hija
from socket import *
import sys
import getopt


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
        print("Mensaje desde el servidor : ", mensajeModificado.decode())
        return mensajeModificado.decode()

    def close(self):
        self.clientSocket.close()


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
        print("Error en los argumentos")
        sys.exit()

    for opt, arg in opts:
        if opt in ['-i', '--ip']:
            ip = arg
        elif opt in ['-n', '--name']:
            name = arg
        elif opt in ['-p', '--port']:
            try:
                port = int(arg)
            except:
                print("Tipo incorrecto debe ser un Int")
                sys.exit()

    return name, ip, port


def game_Phase(palabra):
    # Fase de iniciacion
    # esto lo tengo que mandas asi que en otra funcion mejor
    if palabra == "init":
        print("iniciar partida")
    if len(palabra) == 0:
        print("no combine Code action")

    # Fase de juego
    elif palabra == "turn":
        print("inicio de turno, imprimir combinacion,aciertos y semiaciertos")
    elif palabra == "error":
        print("motivacion")
    elif palabra == "end":
        print("fin de partida")
    elif palabra == "win":
        print("HAS GANADO")


def main():
    name, ip, serverPort = conseguir_argumentos()
    var = ClienteTCP(name, ip, serverPort)
    var.connet()
    x = input("aqui: ")
    var.send(x)
    msg = var.recibir().lower()
    cut = msg.split()
    mensaje = cut[1]
    game_Phase(mensaje.lower())
    var.close()


if __name__ == "__main__":
    main()
