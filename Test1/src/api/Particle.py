import math
from api.GameObject import GameObject
from api.Vector import Vector

class Particle(GameObject):
    
    def __init__(self, aM, aR, aP, aS, aA):
        GameObject.__init__(self)
        
        #Mass (Scalar)
        self.mM = aM
        
        #Radius (Scalar)
        self.mR = aR
        
        #Position (Vector)
        self.mP = aP
        
        #Speed (Vector)
        self.mS = aS
        
        #Acceleration (Vector)
        self.mA = aA
    
    #Mass
    def getM(self):
        return self.mM

    #Radius
    def getR(self):
        return self.mR

    #Position
    def getP(self):
        return self.mP

    #Speed
    def getS(self):
        return self.mS

    #Acceleration
    def getA(self):
        return self.mA
    
    #Mass
    def setM(self, value):
        self.mM = value

    #Radius
    def setR(self, value):
        self.mR = value

    #Position
    def setP(self, value):
        self.mP = value

    #Speed
    def setS(self, value):
        self.mS = value

    #Acceleration
    def setA(self, value):
        self.mA = value
        
    def update(self):
        #Accelerate
        self.mS.sum(self.mA)
        #Move
        self.mP.sum(self.mS)
        
    def destroy(self):
        pass
        
    def bounce(self, p2):
        Particle.Bounce(self, p2)

    @staticmethod
    def CheckCollision(p1, p2):
        #Max distance
        dm = p1.getR() + p2.getR()
        #Cheap check first, real check after
        if abs(p2.getP().getX() - p1.getP().getX()) < dm and abs(p2.getP().getY() - p1.getP().getY()) < dm:
            dr = Vector.Difference(p1.getP(), p2.getP()).getMagnitude()
            if dr >= dm:
                return True
        return False
    
    @staticmethod
    def Bounce(p1, p2):
        dr = Vector.Difference(p1.getP(), p2.getP()).getMagnitude()
        dr.normalize()
        a1 = Vector.AngleRads(p1.getS(), dr)
        a2 = Vector.AngleRads(p2.getS(), dr)
        magS1 = p1.getS().getMagnitude()
        magS2 = p2.getS().getMagnitude()
        s1 = magS1 * math.cos(a1)
        s2 = magS2 * math.cos(a2)
        delta = (2 * (s1 - s2)) / (p1.getM() + p2.getM())
        factor1 = delta * p2.getM()
        factor2 = delta * p1.getM()
        ch1 = dr.multiplyScalar(factor1)
        ch2 = dr.multiplyScalar(factor2)
        p1.getS().substract(ch1)
        p1.getS().sum(ch2)
        