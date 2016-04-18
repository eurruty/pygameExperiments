import math
from api.Point import Point

class Hex(object):
    SQRT3 = 1.73205080757
    S_ANGLE = 0.5
    DR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    DG = [(2, -1), (1, -2), (-1, -1), (-2, 1), (-1, 2), (1, 1)]
    
    
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q -r
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented
        
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __abs__(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Hex(self.q + other.q, self.r + other.r)
        else:
            return NotImplemented
    
    def __iadd__(self, other):
        self.q += other.q
        self.r += other.r
        self.s = -self.q -self.r
        
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Hex(self.q - other.q, self.r - other.r)
        else:
            return NotImplemented
        
    def __isub_(self, other):
        self.q -= other.q
        self.r -= other.r
        self.s = -self.q -self.r
    
    def round(self):
        q = int(round(self.q))
        r = int(round(self.r))
        s = int(round(self.s))
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        else:
            if r_diff > s_diff:
                r = -q - s
            else:
                s = -q - r
        return Hex(q, r)
    
    def add(self, h):
        self.q += h.q
        self.r += h.r
        self.s = -self.q -self.r
        
    def substract(self, h):
        self.q -= h.q
        self.r -= h.r
        self.s = -self.q -self.r
        
    def scale(self, k):
        self.q *= k
        self.r *= k
        self.s = -self.q -self.r
        
    def rotate60(self):
        self.r = -self.q
        self.q = -self.s
        self.s = -self.q -self.r
    
    def getNeighbor(self, d):
        n = Hex(Hex.DR[d])
        n += self
        return n
    
    def getDiagNeighbor(self, d):
        n = Hex(Hex.DG[d])
        n += self
        return n
    
    def getLength(self):
        return self.__abs__()
    
    def getDistance(self, h):
        return h.__sub__(self)
    
    def getCenter(self, o, sz):
        x = int(round(o.x + (sz * Hex.SQRT3 * (self.q + (self.r / 2)))))
        y = int(round(o.y + (sz * 1.5 * self.r)))
        return Point(x, y)
        
    def getCornerOffset(self, sz, cr):
        a = 2.0 * math.pi * ((cr + Hex.S_ANGLE) / 6)
        x = int(round(sz * math.cos(a)))
        y = int(round(sz * math.sin(a)))
        return Point(x, y)
    
    def getCorner(self, o, sz, cr):
        ctr = self.getCenter(o, sz)
        off = self.getCornerOffset(sz, cr)
        x = ctr.x + off.x
        y = ctr.y + off.y
        return Point(x, y)
    
    @staticmethod
    def pixelToHex(p, o, sz):
        pt = Point((p.x - o.x) / sz, (p.y - o.y) / sz)
        q = ((Hex.SQRT3 / 3.0) * pt.x) + ((-1.0 / 3.0) * pt.y)
        r = 1.5 * pt.y
        return Hex(q, r)