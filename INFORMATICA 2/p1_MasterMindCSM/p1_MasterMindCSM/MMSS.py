from socket import *
import threading
import time
import random
import coro as c
import listaEnlazada as lista
from newSocket import *

choir = {} #choir: coro, coral, orfeón #games
id_choir = 0 #id_game
singer_list = lista.listaEnlazada() #client_list
firstCrooner = True


class MMSS(threading.Thread):

    def __init__(self, client_socket, client_addr):
        threading.Thread.__init__(self)
        self.__client_socket = newSocket(client_socket)
        self.__client_addr = client_addr
        self.__nombre = ""
        self.__singer = 0 #jugador
        self.__choir = 0 #partida
        self.end = False

    def createChoir(self):
        global choir, id_choir, singer_list

        #dato = {}
        #dato[self.__client_addr] = id_choir
        #self.__choir = id_choir

        #singer_list.aniadir_fin(dato)

        #En esta versión tenemos un único coro, pero podríamos tener varios coros
        #acompañados de diferentes orquestas.
        choir[id_choir] = c.Coro()
        #choir[id_choir].sockets.append(self.__client_socket)
        #choir[id_choir].singers.append(self.__nombre)
        #id_choir += 1

    def joinChoir(self, id_choir):
        global choir, singer_list

        dato = {}
        dato[self.__client_addr] = id_choir
        self.__choir = id_choir
        singer_list.aniadir_fin(dato)

        choir[id_choir].sockets.append(self.__client_socket)
        choir[id_choir].singers.append(self.__nombre)

    def run(self):

        global firstCrooner

        try:
            while not self.end:
                rcv = self.__client_socket.recv(1024).decode()

                mensaje = rcv.split('#')
                if mensaje[0] == "HELLO":
                    self.__nombre = mensaje[1]

                    if firstCrooner:
                        self.createChoir()
                        firstCrooner = False

                    self.joinChoir(id_choir)
                else:
                    print(self.__nombre + " : " + rcv)

        except ConnectionAbortedError:
            print("Conexión cerrada por el usuario")
            self.end = True