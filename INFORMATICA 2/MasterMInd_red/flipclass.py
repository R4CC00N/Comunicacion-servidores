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
