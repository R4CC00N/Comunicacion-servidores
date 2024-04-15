# HILOS
import threading
import random
import sys


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
        self.combiCode = "nocombiCode"
        self.socket = clientSocket
        self.address = address
        self.end = False

        self.MMC["red"] = "🔴"
        self.MMC["green"] = "📗"
        self.MMC["yellow"] = "🌞"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "🖤"
        self.MMC["white"] = "🤍"
        self.count = 4

        # Todo este codigo aun se puede reutilizar para la otra practica de servidor-cliente

        if len(self.combiCode) == 0:  # si la combinacion a introducir es nula se activa el random code
            self.secretCode = self.randomCode(self.count)
        elif len(self.combiCode) != self.count:
            # si el tamaño de la combinacion introducida es diferente a self.count se activa random code
            self.secretCode = self.randomCode(self.count)
        else:
            try:
                self.secretCode = self.toMasterMindColorCombination(self.combiCode)
            except:
                self.secretCode = self.randomCode(self.count)

    #
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

        """AQUI TIENES QUE CAMBIAR LOS PRINTS POR MENSAJES QUE MANDE EL SERVIDOR AL CLIENTE"""

        fin = False

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
        turn = f"\nTurno {self.currentTurn}"
        m_aciertos = "\nAciertos: " + str(aciertos) + "\n"
        m_parciales = "Aciertos Parciales: " + str(parciales)

        msg = turn + m_aciertos + m_parciales  # puedes añadir mas cosas de los mensajes aqui
        self.socket.send(msg.encode())

        if len(self.secretCode) == aciertos:
            print(f"Has ganado en el turno {self.currentTurn} !!!!")
            self.currentTurn = self.maxTurns
            return

    def run(self):
        """
        SI QUIERES MODIFICAR COSAS ES AQUI O EN UNA FUNCION DE LA CLASE NUEVA
        ADEMAS SI QUIERES PUEDES PONER MAS FORMAS DE MANDAR UN MENSAJE
        TE FALTA EL SECRET CODE Y SI QUIERES OTRO MENSAJE PARA CERRAR EL JUEGO
        """
        num = self.socket.recv(1024).decode()
        codigo = num.split("#")
        self.maxTurns = int(codigo[1])
        print(f"Numero de rondas del cliente : ", codigo[1])

        if codigo[0].lower() == "turns":
            resp = "TURNS#" + codigo[1]
        self.socket.send(resp.encode())
        try:
            while not self.end:
                mensaje = self.socket.recv(1024).decode()
                # print(mensaje)
                codigo = mensaje.split("#")
                # print(codigo)
                if codigo[0].lower() == "colores":
                    self.newTurn(codigo[1])

        except ConnectionError:
            sys.exit('error')
# en el hilo se implementara el mastermind
