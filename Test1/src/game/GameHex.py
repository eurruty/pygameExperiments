from api.Hex import Hex

class GameHex(Hex):
    def __init__(self, q, r, p=True, w=1):
        Hex.__init__(self, q, r)
        self.p = p
        self.w = w