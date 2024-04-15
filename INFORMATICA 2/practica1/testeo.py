from MasterMind011 import MasterMindGame


testGame = MasterMindGame("RGBK")

if testGame.secretCode != ['🔴', '🟢', '🔵', '⚫']:
    print("Error al crear una partida con una combinación concreta.")
else:
    print("Correcto. Ha generado la clave secreta: " + str(['🔴', '🟢', '🔵', '⚫']) + " con la combinación que hemos pedido RGBK.")

print(testGame.secretCode)
print(MasterMindGame("bbbb").secretCode)

print(len("RRRR"))