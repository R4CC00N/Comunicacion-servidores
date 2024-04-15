# HILOS
import sys
import threading
import random


class socketHilo(threading.Thread):
    # MASTERMIND
    # declaramos las variables que vamos a utilizar
    MMC = {}  # diccionario de colores válidos.
    fin = True
    secretCode = []  # código secreto que tenemos que adivinar.

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10  # máximo número de turnos para acertar la clave.
    currentTurn = 0  # turno actual.

    # construimos la función para iniciar la clase
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.combiCode = "nocombicode"
        self.socket = clientSocket
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

        if len(self.combiCode) == 0 or self.combiCode != "nocombicode":  # si la combinacion a introducir es nula se
            # activa el random code
            self.secretCode = self.randomCode(self.count)
        elif len(self.combiCode) != self.count:
            # si el tamaño de la combinacion introducida es diferente a self.count se activa random code
            self.secretCode = self.randomCode(self.count)
        else:
            try:
                self.secretCode = self.toMasterMindColorCombination(self.combiCode)
            except:
                self.secretCode = self.randomCode(self.count)

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
            if self.secretCode[i] == mmcombi[i]:
                cmatches += 1
        return cmatches
        # combinacion = list(map(lambda x, y: x == y, mmcombi, self.secretCode))  # posible uso
        # result = len(list(filter(lambda x: x is True, comprobacion)))

    def countPartialMatches(self, mmcombi: list) -> int:
        smatches = 0
        comprobacion = tuple(map(lambda x, y: (x, x == y), mmcombi, self.secretCode))  # tupla invariable
        lGuess = list(map(lambda x, y: (y, x == y), mmcombi, self.secretCode))  # para modificacion list

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
            self.socket.send(resp.encode())
            return

        # comprobamos si el numero de la combinacion es correcto
        if len(intento) != len(self.secretCode):
            resp = f"Debes hacer una apuesta con {len(self.secretCode)} colores. Por favor, prueba de nuevo."
            self.socket.send(resp.encode())
            return
        # comprobamos si se hagotan turnos

        if self.currentTurn == self.maxTurns or fin:
            resp = "El juego ha terminado, en el turno " + str(
                self.currentTurn) + "\nLo siento, has perdido. Otra vez sera."
            self.socket.send(resp.encode())
            self.end = True
            return

        self.currentTurn += 1

        aciertos = self.countExactMatches(intento)
        parciales = self.countPartialMatches(intento)
        turno = f"\nTurno {self.currentTurn}\n"
        m_aciertos = "Aciertos: " + str(aciertos) + "\n"
        m_semiaciertos = "Aciertos Parciales: " + str(parciales) + "\n"
        m_combi = "Tu combinacion: " + ' '.join(intento) + "\n"
        win = f"Has ganado en el turno {self.currentTurn} !!!!"
        if len(self.secretCode) == aciertos:
            self.currentTurn = self.maxTurns
            self.end = True
            msg = turno + m_combi + m_aciertos + m_semiaciertos + win
            self.socket.send(msg.encode())
            return
        else:
            msg = turno + m_combi + m_aciertos + m_semiaciertos
            self.socket.send(msg.encode())
            return

    def run(self):

        game_init = self.socket.recv(1024).decode()
        codigo = game_init.split("#")
        nombre = codigo[2]
        self.maxTurns = int(codigo[1])
        print(f"Numero de rondas del cliente {nombre}: {codigo[1]}")

        if codigo[0].lower() == "init":
            resp = "Iniciando " + "TURNS#" + codigo[1]
        else:
            resp = "No Iniciando"
        self.socket.send(resp.encode())
        try:
            while not self.end:
                mensaje = self.socket.recv(1024).decode()
                # print(mensaje)
                codigo = mensaje.split("#")
                # print(codigo)
                if codigo[0].lower() == "colors":
                    self.newTurn(codigo[1])
                elif "secretcode" in codigo:
                    print("Creando clave secreta...")
                    self.secretCode = self.toMasterMindColorCombination(codigo[1])
                    my_secret = ' '.join(self.toMasterMindColorCombination(codigo[1]))
                    resp = "su codigo secreto sera: " + my_secret
                    # print("el codigo es: ", self.secretCode)
                    self.socket.send(resp.encode())
                elif codigo[0].lower() == "end":
                    resp = "Terminando comunicacion"
                    self.socket.send(resp.encode())

        except ConnectionError:
            sys.exit("error")
