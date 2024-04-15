from MasterMind import MasterMindGame

#Confía pero comprueba, Raymond Reddington en The Black List.

testGame = MasterMindGame()

print('Probando secret code aleatorio', testGame.secretCode)

if testGame.countExactMatches(testGame.secretCode) != len(testGame.secretCode):
    print("Cuando se genera una clave secreta aleatoria, todos los colores deberían coincidir.")
else:
    print("La clave secreta aleatoria coincide con la clave secreta.")

testGame = MasterMindGame("RGGB")

print('Probando secret code RGGB', testGame.secretCode)

if testGame.countExactMatches(testGame.secretCode) != len(testGame.secretCode):
    print("Cuando se suministra la clave secreta, todos los colores deberían coincidir.")
else:
    print("La clave secreta suministrada coincide con la clave secreta.")


def compareMatches(code: str, guess: str, expected: int):
    game = MasterMindGame(code)

    colors = game.toMasterMindColorCombination(guess)

    nMatches = game.countExactMatches(colors)

    if expected != nMatches:
        print(f"La combinación {guess} debería tener {expected} aciertos con la clave {code} y tenemos {nMatches}")
    else:
        print(f"La combinación {guess} tiene {nMatches} aciertos que coincide con lo esperado {expected} aciertos para la clave {code}")

compareMatches("RGGB", "RGGB", 4)

compareMatches("RGGB", "KKKK", 0)
compareMatches("RGGB", "GGGG", 2)
compareMatches("RGGB", "RBBB", 2)
compareMatches("RGGB", "GRRG", 0)
compareMatches("RGGB", "KGBY", 1)
compareMatches("RGGB", "GGBG", 1)