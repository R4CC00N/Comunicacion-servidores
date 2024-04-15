# HILOS
import sys
import threading
import random
from newSocket import *
import Lista_Enlazada as lista

client_list = lista.listaEnlazada()
socket_comunicacion = []
finGame = 0


class socketHilo(threading.Thread):
    # MASTERMIND
    # declaramos las variables que vamos a utilizar
    MMC = {}  # diccionario de colores válidos.
    fin = True
    secretCode = []  # código secreto que tenemos que adivinar.

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10  # máximo número de turnos para acertar la clave.
    currentTurn = 0  # turno actual.

    partidas_in_game = {}  # partidas creadas que tengan 2 jugadores
    partidas = {}  # partidas creadas que solo tengan 1 jugador

    sockets_list = []  # proxima modificacion para que no haya errores de jugabilidad
    id_partidas = []

    # construimos la función para iniciar la clase
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.combiCode = "nocombicode"
        self.socket = newSocket(clientSocket)
        self.address = address
        self.end = False

        # MASTERMIND
        self.MMC["red"] = "🔴"
        self.MMC["green"] = "📗"
        self.MMC["yellow"] = "🌞"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "🖤"
        self.MMC["white"] = "🤍"
        self.count = 4

        # if len(self.combiCode) == 0 or self.combiCode != "nocombicode":  # si la combinacion a introducir es nula se
        #     # activa el random code
        #     self.secretCode = self.randomCode(self.count)
        # elif len(self.combiCode) != self.count:
        #     # si el tamaño de la combinacion introducida es diferente a self.count se activa random code
        #     self.secretCode = self.randomCode(self.count)
        # else:
        #     try:
        #         self.secretCode = self.toMasterMindColorCombination(self.combiCode)
        #     except:
        #         self.secretCode = self.randomCode(self.count)

    def randomCode(self, val):  # genera un código aleatorio
        return random.choices(self.toMasterMindColorCombination(self.validColors), k=val)

    def MasterMindColor(self, color: str):  # convertir cadenas en colores
        # color r, g, y, b, k ,w
        rcolor = "Color no encontrado."

        if color == "red" or color == "r" or color == "R" or color == "🔴":
            rcolor = self.MMC["red"]
        elif color == "green" or color == "g" or color == "G" or color == "📗":
            rcolor = self.MMC["green"]
        elif color == "yellow" or color == "y" or color == "Y" or color == "🌞":
            rcolor = self.MMC["yellow"]
        elif color == "blue" or color == "b" or color == "B" or color == "🔵":
            rcolor = self.MMC["blue"]
        elif color == "black" or color == "k" or color == "K" or color == "🖤":
            rcolor = self.MMC["black"]
        elif color == "white" or color == "w" or color == "W" or color == "🤍":
            rcolor = self.MMC["white"]
        else:

            raise KeyError(rcolor)

        return rcolor

    def toMasterMindColorCombination(self, convinacion):  # obtener una cadena de selfes mastermind
        return list(map(lambda n: self.MasterMindColor(n), convinacion))

    def countExactMatches(self, mmcombi: list) -> int:
        cmatches = 0
        for i in range(0, len(mmcombi)):
            if code_play[i] == mmcombi[i]:
                cmatches += 1
        return cmatches
        # combinacion = list(map(lambda x, y: x == y, mmcombi, self.secretCode))  # posible uso
        # result = len(list(filter(lambda x: x is True, comprobacion)))

    def countPartialMatches(self, mmcombi: list) -> int:
        smatches = 0
        comprobacion = tuple(map(lambda x, y: (x, x == y), mmcombi, code_play))  # tupla invariable
        lGuess = list(map(lambda x, y: (y, x == y), mmcombi, code_play))  # para modificacion list

        def countMatches(x) -> tuple:
            isCheck = False
            if lGuess.__contains__(x) and not x[1]:
                index = lGuess.index(x)
                if not comprobacion[index][1]:
                    lGuess[index] = (x[0], True)
                    isCheck = True
            return x[0], isCheck

        tsMatches = tuple(map(lambda x: countMatches(x), comprobacion))
        for x in tsMatches:
            if x[1]:
                smatches += 1
        return smatches

    def newTurn(self, guess):

        fin = False
        # comprobamos si la combinacion es valida

        try:
            intento = self.toMasterMindColorCombination(guess)

        except:
            resp = "Combinación incorrecta. Por favor, prueba de nuevo. \n"
            socket_comunicacion[0].send(resp.encode("utf-8"))
            socket_comunicacion[1].send(resp.encode("utf-8"))
            return

        # comprobamos si el numero de la combinacion es correcto
        if len(intento) != len(code_play):
            resp = f"Debes hacer una apuesta con {len(code_play)} colores. Por favor, prueba de nuevo."
            socket_comunicacion[0].send(resp.encode("utf-8"))
            socket_comunicacion[1].send(resp.encode("utf-8"))
            return
        # comprobamos si se hagotan turnos

        if self.currentTurn == game_turn or fin:
            resp = "El juego ha terminado, en el turno " + str(
                self.currentTurn) + "\nLo siento, has perdido. Otra vez sera, cambio de turno"
            socket_comunicacion[0].send(resp.encode("utf-8"))
            socket_comunicacion[1].send(resp.encode("utf-8"))
            self.end = False

            return

        self.currentTurn += 1

        aciertos = self.countExactMatches(intento)
        parciales = self.countPartialMatches(intento)
        cambio = "\ncambio de turno"
        turno = f"\nTurno {self.currentTurn}\n"
        m_aciertos = "Aciertos: " + str(aciertos) + "\n"
        m_semiaciertos = "Aciertos Parciales: " + str(parciales) + "\n"
        m_combi = "Tu combinacion: " + ' '.join(intento) + "\n"
        win = f"Has ganado en el turno {self.currentTurn} !!!!"
        if len(code_play) == aciertos:
            self.currentTurn = game_turn
            self.end = False
            msg = turno + m_combi + m_aciertos + m_semiaciertos + win + cambio
            # print("ojooooooooooooo",socket_comunicacion)
            self.socket.send(msg.encode("utf-8"))
            socket_comunicacion[1].send(msg.encode("utf-8"))

            # podriamos aplicar boolean para cambiar el juego
            return
        else:
            msg = turno + m_combi + m_aciertos + m_semiaciertos
            self.socket.send(msg.encode("utf-8"))
            socket_comunicacion[1].send(msg.encode("utf-8"))
            return

    def seleccion_partida(self):
        for i in range(len(self.id_partidas)):
            self.partidas_in_game[i + 1] = self.sockets_list[i]

    def menu_partidas(self):
        for i in range(len(self.id_partidas)):
            msj = f"partida de {self.id_partidas[i]}"
            self.partidas[i + 1] = msj

    # PRINCIPAL

    def run(self):

        # SOLUCIONAR EL ERROR CUANDO SE UNE A UNA PARTIDA PARA ELLO LAS PARTIDAS YA EN JUEGO SE UNIRAN A UN
        # DICCIONARIO O LISTA ENLAZADA CON NOMBRE Y SOCKET ¿LISTA ENLAZADA CON ESTO PARA EL JUEGO?
        global game_turn
        global code_play
        global socket_comunicacion
        global finGame
        # lista de jugadores
        # print(self.sockets_list)
        # print(str(self.address()))
        game_init = self.socket.recv(1024).decode()
        codigo = game_init.split("#")
        if len(codigo) > 1:
            nombre = codigo[2]
        else:
            pass
        if codigo[0].lower() == "hello":
            client_list.aniadir_frente(nombre)
            print(game_init)
            self.sockets_list.append(self.socket)
            self.id_partidas.append(nombre)
            print("id_partidas: ", self.id_partidas)
            print("llego")
        recive = self.socket.recv(1024).decode()
        codigo = recive.split("#")
        if codigo[0].lower() == "init":
            resp = "Iniciando " + "TURNS#" + codigo[1]
            print(f"Numero de rondas del cliente {nombre}: {codigo[1]}")
            self.menu_partidas()
            self.seleccion_partida()
            print(self.partidas_in_game)
            self.socket.send(resp.encode("utf-8"))
            self.maxTurns = int(codigo[1])
            game_turn = self.maxTurns
        elif codigo[0].lower() == "unirse":
            mensaje_menu = f"Estos son las partidas vacias: \n{self.partidas}"
            self.socket.send(mensaje_menu.encode("utf-8"))
            recive = self.socket.recv(1024).decode()
            codigo = recive.split("#")
            if codigo[0].lower() == "id":
                print(self.partidas.keys())
                unir_partida = codigo[1]
                print(unir_partida)
                if int(codigo[1]) in self.partidas.keys():
                    self.partidas_in_game[int(codigo[1])] = [self.partidas_in_game.get(int(codigo[1])), self.socket]
                    socket_comunicacion = self.partidas_in_game[int(codigo[1])]
                    self.partidas.pop(int(codigo[1]))
                    self.id_partidas.pop(int(codigo[1]))
                    resp = "Uniendose a la partida: " + "#" + codigo[1]
                    self.socket.send(resp.encode("utf-8"))
                else:
                    resp = "No se a podido unir a la partida: " + codigo[1]
                    self.socket.send(resp.encode("utf-8"))
        else:
            resp = "No Iniciando"
            self.socket.send(resp.encode("utf-8"))
        try:

            while not self.end:
                print("contador: ", finGame)
                mensaje = self.socket.recv(1024).decode()
                print(mensaje)
                codigo = mensaje.split("#")
                # print(codigo)
                if codigo[0].lower() == "colors":
                    self.newTurn(codigo[1])
                elif "cambio" in codigo:
                    finGame += 1
                    # print(codigo)
                    socket_comunicacion = socket_comunicacion[::-1]
                    # print(socket_comunicacion)
                    resp = "cambio"
                    socket_comunicacion[0].send(resp.encode("utf-8"))
                    socket_comunicacion[1].send(resp.encode("utf-8"))
                    if finGame == 2:
                        resp = "Terminando juego"
                        print(resp)
                        socket_comunicacion[0].send(resp.encode("utf-8"))
                        socket_comunicacion[1].send(resp.encode("utf-8"))
                        self.end = True

                elif "secretcode" in codigo:
                    print("Creando clave secreta...")
                    # print(self.partidas_in_game)
                    # print(self.partidas)
                    self.secretCode = self.toMasterMindColorCombination(codigo[1])
                    code_play = self.secretCode
                    resp = "listo"
                    # cambiar esto por self.partidas_in_game.get[id][0] o [1]
                    socket_comunicacion[0].send(resp.encode("utf-8"))
                    socket_comunicacion[1].send(resp.encode("utf-8"))
                    my_secret = ' '.join(self.toMasterMindColorCombination(codigo[1]))
                    resp = "su codigo secreto sera: " + my_secret
                    # print("el codigo es: ", self.secretCode)
                    socket_comunicacion[1].send(resp.encode("utf-8"))

                elif codigo[0].lower() == "end":
                    resp = "Terminando comunicacion"
                    self.socket.send(resp.encode("utf-8"))
        except ConnectionError:
            sys.exit("error")
