from MasterMind02 import MasterMindGame

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

def comparePartialMatches(code: str, guess: str, expected: int):
    game = MasterMindGame(code)

    colors = game.toMasterMindColorCombination(guess)

    nMatches = game.countPartialMatches(colors)

    if expected != nMatches:
        print(f"La combinación {guess} debería tener {expected} semiaciertos con la clave {code} y tenemos {nMatches}")
    else:
        print(f"La combinación {guess} tiene {nMatches} semiaciertos que coincide con lo esperado {expected} semiaciertos para la clave {code}")

comparePartialMatches("RGGB", "RGGB", 0)

comparePartialMatches("RGGB", "KKKK", 0)
comparePartialMatches("RGGB", "GGGG", 0)
comparePartialMatches("RGGB", "RBBB", 0)
comparePartialMatches("RGGB", "GRRG", 3)
comparePartialMatches("RGGB", "KGBY", 1)
comparePartialMatches("RGGB", "GGBG", 2)