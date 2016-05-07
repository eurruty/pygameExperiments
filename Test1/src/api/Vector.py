import math

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
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
    
    def __str__(self):
        return ("[" + str(self.x) + ", " + str(self.y) + "]")
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented
        
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented
        
    def __isub__(self, other):
        return self.__sub__(other)
    
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
        
    def setX(self, value):
        self.x = value

    def setY(self, value):
        self.y = value
        
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def getMagnitude(self):
        return (self.x**2 + self.y**2)**(0.5)
    
    def getAngleRads(self):
        return math.pi - math.atan2(self.y, self.x)
    
    def getAngleDegs(self):
        return math.degrees(self.getAngleRads())
    
    def getNormal(self):
        normal = Vector(self.x, self.y)
        normal.normalize()
        return normal
    
    def normalize(self):
        mag = self.getMagnitude()
        self.x /= mag
        self.y /= mag
        return mag
    
    def invert(self):
        self.x = -self.x
        self.y = -self.y
        
    def rotateRads(self, angleRads):
        cos = math.cos(angleRads)
        sin = math.sin(angleRads)
        
        newX = (self.x * cos) - (self.y * sin)
        newY = (self.x * sin) + (self.y * cos)
        
        self.x = newX
        self.y = newY
        
    def setAngleRads(self, angleRads):
        self.x = abs(self)
        self.y = 0
        self.rotateRads(angleRads)
    
    def rotateDegs(self, angleDegs):
        angleRads = math.radians(angleDegs)
        self.rotateRads(angleRads)
        
    def setAngleDegs(self, angleDegs):
        self.x = abs(self)
        self.y = 0
        self.rotateDegs(angleDegs)
    
    def sum(self, v):
        self.x += v.getX()
        self.y += v.getY()
        
    def substract(self, v):
        self.x -= v.getX()
        self.y -= v.getY()
        
    def multiplyScalar(self, s):
        self.x *= s
        self.y *= s

    def delX(self):
        del self.x

    def delY(self):
        del self.y

    def destroy(self):
        pass
    
    @staticmethod
    def Difference(v1, v2):
        return Vector(v2.getX() - v1.getX(), v2.getY() - v1.getY())
    
    @staticmethod
    def ScalarProduct(v1, v2):
        return (v1.getX() * v2.getX()) + (v1.getY() * v2.getY())
    
    @staticmethod
    def AngleRads(v1, v2):
        s = Vector.ScalarProduct(v1, v2)
        if s == 0:
            return math.pi / 2
        
        m1 = v1.getMagnitude()
        m2 = v2.getMagnitude()
        if m1 == 0 or m2 == 0:
            return 0
        
        return math.pi - math.acos(s / m1 * m2)
    
    @staticmethod
    def AngleDegs(v1, v2):
        return math.degrees(Vector.AngleRads(v1, v2))