import math

class Vector(object):
    def __init__(self, aX, aY):
        self.mX = aX
        self.mY = aY
        
    def setX(self, value):
        self.mX = value

    def setY(self, value):
        self.mY = value
        
    def getX(self):
        return self.mX

    def getY(self):
        return self.mY
    
    def getMagnitude(self):
        return (self.mX**2 + self.mY**2)**(0.5)
    
    def getAngleRads(self):
        return math.pi - math.atan2(self.mY, self.mX)
    
    def getAngleDegs(self):
        return math.degrees(self.getAngleRads())
    
    def getNormal(self):
        normal = Vector(self.mX, self.mY)
        normal.normalize()
        return normal
    
    def normalize(self):
        mag = self.getMagnitude()
        self.mX /= mag
        self.mY /= mag
        return mag
    
    def invert(self):
        self.mX = -self.mX
        self.mY = -self.mY
    
    def sum(self, v):
        self.mX += v.getX()
        self.mY += v.getY()
        
    def substract(self, v):
        self.mX -= v.getX()
        self.mY -= v.getY()
        
    def multiplyScalar(self, s):
        self.mX *= s
        self.mY *= s

    def delX(self):
        del self.mX

    def delY(self):
        del self.mY

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
    
    