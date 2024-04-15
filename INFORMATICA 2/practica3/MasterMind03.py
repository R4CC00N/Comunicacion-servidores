import random


# esqueleto inicial
class MasterMindGame:
    # declaramos las variables que vamos a utilizar
    maxTurns = 10
    MMC = {}  # diccionario de colores válidos.
    fin = True
    secretCode = []  # código secreto que tenemos que adivinar.

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10  # máximo número de turnos para acertar la clave.
    currentTurn = 0  # turno actual.

    # construimos la función para iniciar la clase
    def __init__(self, combiCode: str = "nocombiCode"):
        # iniciamos el diccionario de colores
        self.MMC["red"] = "🔴"
        self.MMC["green"] = "📗"
        self.MMC["yellow"] = "🌞"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "🖤"
        self.MMC["white"] = "🤍"
        self.count = 4

        # Todo este codigo aun se puede reutilizar para la otra practica de servidor-cliente

        if len(combiCode) == 0:  # si la combinacion a introducir es nula se activa el random code
            self.secretCode = self.randomCode(self.count)
        elif len(combiCode) != self.count:
            # si el tamaño de la combinacion introducida es diferente a self.count se activa random code
            self.secretCode = self.randomCode(self.count)
        else:
            try:
                self.secretCode = self.toMasterMindColorCombination(combiCode)
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
        combinacion_pc = self.secretCode
        combinacion_payer = []  # trabajamos con esto para mostrar resultados ya que mmcombi cambia
        for i in range(0, len(mmcombi)):
            combinacion_payer.append(mmcombi[i])
            if combinacion_pc[i] in mmcombi:  # mmcombi[i] in combinacion:
                # revisamos dentro de las combinaciones del pc y el player
                if combinacion_pc[i] == mmcombi[i]:
                    # si son iguales cambia el valord e uno de ellos para que no sea parte de los resultados validos
                    mmcombi[i] = 0
                elif combinacion_pc[i] != mmcombi[i]:  # si son diferentes suma 1
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


if __name__ == "__main__":
    testGame = MasterMindGame()
    secreto = testGame.secretCode

    while testGame.currentTurn != testGame.maxTurns:
        x = input("Ingresa tu codigo: ")
        testGame.newTurn(x)
        print("secreto: ", ' '.join(secreto))
