from api.Hex import Hex

class GameHex(Hex):
    
    STATE_DISABLED = 0
    STATE_PASSABLE = 1
    STATE_IMPASSABLE = 2
    HEX_TYPES = [STATE_DISABLED, STATE_PASSABLE, STATE_IMPASSABLE]
    
    def __init__(self, q, r, p=STATE_PASSABLE, w=0):
        Hex.__init__(self, q, r)
        self.state = p
        self.w = w