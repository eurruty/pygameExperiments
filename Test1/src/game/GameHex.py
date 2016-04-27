from api.Hex import Hex

class GameHex(Hex):
    
    DISABLED = -1
    PASSABLE = 0
    IMPASSABLE = 1
    HEX_TYPES = [DISABLED, PASSABLE, IMPASSABLE]
    
    def __init__(self, q, r, p=PASSABLE, w=1):
        Hex.__init__(self, q, r)
        self.p = p
        self.w = w