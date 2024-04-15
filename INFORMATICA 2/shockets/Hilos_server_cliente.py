# HILOS
import threading


class socketHilo(threading.Thread):
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.socket = clientSocket
        self.address = address

        # podemos meter el mastermind __init__

    def run(self):
        # fases inicializacion, clave, juego
        while True:
            mensaje = self.socket.recv(1024).decode()
            self.socket.send(mensaje.encode())

# en el hilo se implementara el mastermind