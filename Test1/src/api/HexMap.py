from Hex import Hex

class HexMap(object):
    def __init__(self, h, w):
        #define map
        self.map = [None] * h
        for i in range(h):
            self.map[i] = [None] * w
        
        #fill map
        for i in range(h):
            for j in range(w):
                first = -(i // 2)
                q = first + j
                r = i
                self.map[i][j] = Hex(q, r)
    
    def getHex(self, q, r):
        x = q - (r // 2)
        y = r
        return self.map[x][y]
    
    def setHex(self, h):
        x = h.q - (h.r // 2)
        y = h.r
        self.map[x][y] = h