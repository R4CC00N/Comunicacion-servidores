from MasterMind03 import MasterMindGame

# inicializamos el mastermind
game = MasterMindGame("RGBK")
# Codigo secreto en str
sCode = ' '.join(game.secretCode)

# print("**********************************************************")
# print("Test 0: Comprobamos el secret code")
# game.newTurn("rbbr")
# print("secret Code: ", sCode)


# print("**********************************************************")
# print("Test 1: Comprobamos si la combinacion es correcta")
# game.newTurn("rgbk")

# print("**********************************************************")
# print("Test 2: Comprobamos si la longitud es correcta")
# game.newTurn("rrrrrr")

print("**********************************************************")
print("Test 3: probamos jugar")
print("---------------------------------")
game.newTurn("rrrr")
print("Deberia haber 1 acierto y ningun parcial")
print("---------------------------------")
game.newTurn("rrrb")
print("Deberia haber 1 acierto y 1 parcial")
print("---------------------------------")
game.newTurn("rrbr")
print("Deberia haber 2 acierto y ningun parcial")
print("---------------------------------")
game.newTurn("rkbg")
print("Deberia haber 2 acierto y 2 parcial")
print("---------------------------------")
game.newTurn("rgbbk")
print("Deberia haber un error de tamaño")
print("---------------------------------")
game.newTurn("rgbk")
print("Deberia haber 4 acierto y terminar el juego")