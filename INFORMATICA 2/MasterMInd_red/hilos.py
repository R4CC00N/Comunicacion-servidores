# HILOS
import threading
import random


class socketHilo(threading.Thread):
    # declaramos las variables que vamos a utilizar
    maxTurns = 10
    MMC = {}  # diccionario de colores válidos.
    fin = True
    secretCode = []  # código secreto que tenemos que adivinar.

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10  # máximo número de turnos para acertar la clave.
    currentTurn = 0  # turno actual.

    # construimos la función para iniciar la clase
    def __init__(self, clientSocket, address):
        threading.Thread.__init__(self)
        self.socket = clientSocket
        self.address = address

        # iniciamos el diccionario de colores
        self.MMC["red"] = "🔴"
        self.MMC["green"] = "📗"
        self.MMC["yellow"] = "🌞"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "🖤"
        self.MMC["white"] = "🤍"
        self.count = 4

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
        intento = []
        # comprobamos si la combinacion es valida

        try:
            intento = self.toMasterMindColorCombination(guess)
        except:
            print("Combinación incorrecta. Por favor, prueba de nuevo.")
            return

        print("Tu combinacion: ", ' '.join(intento))
        # comprobamos si el numero de la combinacion es correcto

        if len(intento) != len(self.secretCode):
            print(f"Debes hacer una apuesta con {len(self.secretCode)} colores. Por favor, prueba de nuevo.")
            return
        # comprobamos si se hagotan turnos

        if self.currentTurn == self.maxTurns or fin:
            print("El juego ha terminado")
            print("Lo siento, has perdido. Otra vez sera.")
            return
        self.currentTurn += 1
        aciertos = self.countExactMatches(intento)
        parciales = self.countPartialMatches(intento)
        print("Aciertos: ", aciertos)
        print("Aciertos Parciales: ", parciales)
        if len(self.secretCode) == aciertos:
            print(f"Has ganado en el turno {self.currentTurn} !!!!")
            self.currentTurn = self.maxTurns
            return

        if len(intento) == 0:
            print("Combinación incorrecta. Por favor, prueba de nuevo.")
            return
        else:
            print(f"Turno {self.currentTurn}")
            return

    def process_msg(self, mensaje):
        msgtotal = mensaje.decode().lower()
        cut = msgtotal.split()
        name = cut[0]
        clave = cut[1]
        intento = cut[2]
        return name, clave, intento

    def init_phase(self, mensaje):
        name, clave, intento = self.process_msg(mensaje)
        msg = f"el usuario {name.upper()} con la clave: ({clave})"
        if clave == "init":
            self.maxTurns = intento
            mensaje = msg + " Iniciado"
            self.socket.send(mensaje.encode())
            return True
        else:
            msg = "No iniciado"
            self.socket.send(msg.encode())
            return False
        self.socket.close()

    def game_phase(self, mensaje):
        name, clave, intento = self.process_msg(mensaje)
        if clave != "noconbinecode" or len(clave) == 0:
            if len(intento) == 0:  # si la combinacion a introducir es nula se activa el random code
                self.secretCode = self.randomCode(self.count)
                self.socket.send("no pa".encode())
            elif len(intento) != self.count:
                # si el tamaño de la combinacion introducida es diferente a self.count se activa random code
                self.secretCode = self.randomCode(self.count)
                self.socket.send("no pa".encode())
            else:
                try:
                    self.secretCode = self.toMasterMindColorCombination(intento)
                    self.socket.send(intento.encode())
                    self.socket.send(self.secretCode.encode())
                except:
                    self.secretCode = self.randomCode(self.count)
                    self.socket.send("creado".encode())
        if clave == "noconbinecode":
            self.secretCode = self.randomCode(self.count)
            msg = "No existe clave se generara una: " + self.secretCode
            self.socket.send(msg.encode())

    def run(self):

        # fases inicializacion, clave, juego
        while True:
            mensaje = self.socket.recv(1024)
            if self.init_phase(mensaje):
                self.game_phase(mensaje)

# en el hilo se implementara el mastermind
