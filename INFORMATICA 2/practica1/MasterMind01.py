import random


# esqueleto inicial
class MasterMindGame:
    # declaramos las variables que vamos a utilizar

    MMC = {}  # diccionario de colores válidos.

    secretCode = []  # código secreto que tenemos que adivinar.

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10  # máximo número de turnos para acertar la clave.
    currentTurn = 0  # turno actual.

    # construimos la función para iniciar la clase
    def __init__(self, combiCode: str = "nocombiCode"):
        # iniciamos el diccionario de colores
        self.MMC["red"] = "🔴"
        self.MMC["green"] = "🟢"
        self.MMC["yellow"] = "🟡"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "⚫"
        self.MMC["white"] = "⚪"

        if len(combiCode) == 0:  # si la combinacion a introducir es nula se activa el random code
            self.secretCode = self.randomCode(4)
        elif len(combiCode) != 4:  # si el tamaño de la combinacion introducida es diferente a 4 se activa random code
            self.secretCode = self.randomCode(4)
        else:
            try:
                self.secretCode = self.toMasterMindColorCombination(combiCode)
            except:
                self.secretCode = self.randomCode(4)

    #
    def randomCode(self, val):  # genera un código aleatorio
        return random.choices(self.toMasterMindColorCombination(self.validColors), k=val)

    def MasterMindColor(self, color: str):  # convertir cadenas en colores
        # color r, g, y, b, k ,w
        rcolor = "Color no encontrado."
        # validaciones para todos los colores y las pocibles entradas de este
        if color == "red" or color == "r" or color == "R" or color == "🔴":
            rcolor = self.MMC["red"]
        elif color == "green" or color == "g" or color == "G" or color == "🟢":
            rcolor = self.MMC["green"]
        elif color == "yellow" or color == "y" or color == "Y" or color == "🟡":
            rcolor = self.MMC["yellow"]
        elif color == "blue" or color == "b" or color == "B" or color == "🔵":
            rcolor = self.MMC["blue"]
        elif color == "black" or color == "k" or color == "K" or color == "⚫":
            rcolor = self.MMC["black"]
        elif color == "white" or color == "w" or color == "W" or color == "⚪":
            rcolor = self.MMC["white"]
        else:
            raise KeyError(rcolor)
        return rcolor

    def toMasterMindColorCombination(self, convinacion):  # obtener una cadena de selfes mastermind y convertirla a emojis
        return list(map(lambda n: self.MasterMindColor(n), convinacion))


if "__name__" == "__main__":
    x = MasterMindGame()
    print(x.MasterMindColor("r"))
