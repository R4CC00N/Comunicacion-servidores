from socket import *
from hilos_coin import *
import sys
import getopt


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


def conseguir_argumentos():
    ip = "127.0.0.1"
    port = 1234

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "i:p:", ["ip =", "port ="])
        if len(argv) < 2:
            print("Faltan valores")
            sys.exit()
    except:
        print("Error en los argumentos")
        sys.exit()

    for opt, arg in opts:
        if opt in ['-i', '--ip']:
            ip = arg
        elif opt in ['-p', '--port']:
            try:
                port = int(arg)
            except:
                print("Tipo incorrecto debe ser un Int")
                sys.exit()

    return ip, port


def main():
    localhost, serverPort = conseguir_argumentos()
    server = ServerTCP(localhost, serverPort)
    server.crearServer()
    server.comunicacion()


if __name__ == "__main__":
    main()
