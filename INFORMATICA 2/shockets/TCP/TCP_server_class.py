from socket import *


# from Hilos_server_cliente import *

class ServerTCP:
    def __init__(self, host, sPort=12000):
        self.host = host
        self.port = sPort
        self.serverSocket = None

    def connect(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)  # Solicitudes en cola
        print("El servidor esta listo para ser usado", self.port)

    def use(self):
        while True:
            clientsocket, direccion = self.serverSocket.accept()  # acepta la conexion del cliente
            # hilo = socketHilo(clientsocket, direccion)  # importante para hilos
            mensaje = clientsocket.recv(1024)
            print(mensaje.decode())
            msg = mensaje.decode().upper()
            clientsocket.send(msg.encode())
            print("conexion desde: ", direccion)
            print()
            # hilo.start()

    def diconnect_Socket(self):
        self.serverSocket.close()


def main():
    serverPort = 1200
    localhost = "127.0.0.1"
    server = ServerTCP(localhost, serverPort)
    server.connect()
    server.use()
    server.diconnect_Socket()


if __name__ == "__main__":
    main()
