import math
from api.Vector import Vector
from api.GameObject import GameObject

class Hex(GameObject):
    
    SQRT3 = 3.0**0.5
    #SQRT3 = 7.0/4.0
    
    # ~30 CCW
    S_ANGLE = 0.5
    
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = (-q) + (-r)
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.q == other.q and self.r == other.r and self.s == other.s)
        else:
            return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented
        
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __str__(self):
        return ("[" + str(self.q) + ", " + str(self.r) + ", " + str(self.s) + "]")
    
    def __abs__(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Hex(self.q + other.q, self.r + other.r)
        else:
            return NotImplemented
    
    def __iadd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Hex(self.q - other.q, self.r - other.r)
        else:
            return NotImplemented
        
    def __isub__(self, other):
        return self.__sub__(other)
        
    def getAxialCoords(self):
        return(self.q, self.r)
    
    def add(self, h):
        self += h
        
    def substract(self, h):
        self -= h
    
    def getCenter(self, o, sz):
        x = o.x + (sz * Hex.SQRT3 * (self.q + (self.r / 2.0)))
        y = o.y + (sz * (3.0 / 2.0) * self.r)
        return Vector(x, y)
        
    def getCornerOffset(self, sz, cr):
        a = 2.0 * math.pi * ((cr + Hex.S_ANGLE) / 6)
        x = sz * math.cos(a)
        y = sz * math.sin(a)
        return Vector(x, y)
    
    def getCornerOffsets(self, sz):
        corners = []
        for x in range(0, 6):
            corners.append(self.getCornerOffset(sz, x))
        return corners
    
    def getCorner(self, o, sz, cr):
        ctr = self.getCenter(o, sz)
        off = self.getCornerOffset(sz, cr)
        x = ctr.x + off.x
        y = ctr.y + off.y
        return Vector(x, y)
    
    def getCorners(self, o, sz):
        ctr = self.getCenter(o, sz)
        corners = []
        for x in range(0, 6):
            corners.append(ctr + self.getCornerOffset(sz, x))
        return corners
    
    def getCornersAsList(self, o, sz):
        ctr = self.getCenter(o, sz)
        corners = []
        for x in range(0, 6):
            p = ctr + self.getCornerOffset(sz, x)
            corners.append((p.x, p.y))
        return corners
    
    def getCornersStroked(self, o, sz):
        ctr = self.getCenter(o, sz)
        corners = []
        for x in range(0, 6):
            p = ctr + self.getCornerOffset(sz - 2, x)
            corners.append((p.x, p.y))
        return corners
    
    def round(self):
        q = int(round(self.q))
        r = int(round(self.r))
        s = int(round(self.s))
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = (-r) + (-s)
        else:
            if r_diff > s_diff:
                r = (-q) + (-s)
            else:
                s = (-q) + (-r)
        self.q = q
        self.r = r
        self.s = s
    
    @staticmethod
    def pixelToHex(p, o, sz):
        pt = Vector(p.x - o.x, p.y - o.y)
        q = ((pt.x * Hex.SQRT3 / 3.0) - (pt.y / 3.0)) / (sz * 1.0)
        r = (pt.y * 2.0 / 3.0) / (sz * 1.0)
        h = Hex(q, r)
        h.round()
        return h