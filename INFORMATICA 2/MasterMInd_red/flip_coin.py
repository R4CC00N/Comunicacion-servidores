import random


class flipcoin:
    coin = {}

    def __init__(self):
        self.coin["cara"] = 1
        self.coin["cruz"] = 2

    def parseMyplif(self, flip: str) -> str:
        flipcode = 0
        if flip.lower() == "cara":
            flipcode = self.coin[flip.lower()]
        elif flip.lower() == "cruz":
            flipcode = self.coin[flip.lower()]
        elif flip.lower() == "fin":
            flipcode = -1
        return str(flipcode)

    def checkflip(self, flip):
        flipcoin = random.randint(1, 2)
        if int(flip) == flipcoin:
            resp = "HAS ACERTADO"
        else:
            resp = "FALLO"
        return resp

    def play(self):
        fin = False
        while not fin:
            msg = input("cara o cruz:  ")
            parsemsg = self.parseMyplif(msg)
            if parsemsg == "-1":
                fin = True
                print("bye")
            if parsemsg == "0":
                print("otra vez")
            elif not fin:
                print(self.checkflip(parsemsg))

if __name__ == "__main__":
    turno = flipcoin()
    turno.play()