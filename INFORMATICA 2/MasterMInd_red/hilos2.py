# HILOS
import threading
import random


class socketHilo(threading.Thread):

    # construimos la función para iniciar la clase
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.socket = clientSocket
        self.address = address

    def run(self):
        # fases inicializacion, clave, juego
        mensaje = self.socket.recv(1024).decode()
        print(mensaje)
        codigo = mensaje.split("#")
        print(codigo)
        if codigo[0] == "TURNS":
            msg = "TURNS#" + codigo[1]
            self.socket.send(msg.encode())

# en el hilo se implementara el mastermind
