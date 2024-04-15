# HILOS
import sys
import threading
import random
from newSocket import *


class socketHilo(threading.Thread):

    # construimos la función para iniciar la clase
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.socket = newSocket(clientSocket)
        self.address = address
        self.end = False

    def run(self):
        # fases inicializacion, clave, juego
        try:
            while not self.end:
                mensaje = self.socket.recv(1024).decode()
                print(mensaje)
                flipcoin = random.randint(1, 2)
                if mensaje == "-1":
                    self.end = True
                    # self.socket.close()
                if self.end:
                    resp = "adios"
                else:
                    if int(mensaje) == flipcoin:
                        resp = "HAS ACERTADO"
                        # self.end = True # cierra la comunicacion si pasa esto
                    else:
                        if int(mensaje) != flipcoin:
                            resp = "FALLO"

                self.socket.send(resp.encode())

        except ConnectionError:
            sys.exit("error")

# en el hilo se implementara el mastermind
