# -*- coding: utf-8 -*-
import pygame
from api.Particle import Particle

class ParticleSprite(Particle):
    
    # Constructor.
    def __init__(self, aM, aP, aS, aA, aImgFile):
        # Imagen
        self.mImg = None
        self.mImg = pygame.image.load(aImgFile)
        self.mImg = self.mImg.convert_alpha()

        # Rectángulo
        self.mImgRect = self.mImg.get_rect()
        
        # Radio
        aR = (self.mImgRect.width + self.mImgRect.height) // 4
        self.hitboxRadius = aR

        Particle.__init__(self, aM, aR, aP, aS, aA)

        # Ángulo
        self.mAngle = 0

        # Velocidad angular
        self.mAngularSpeed = 0

        # Aceleración angular
        self.mAngularAccel = 0

        # Auxiliar para imagen girada
        self.mDisplayImg = self.mImg
        self.mDisplayAngle = self.mAngle

    # Update
    def update(self):
        Particle.update(self)
        
        self.mAngularSpeed += self.mAngularAccel
        
        self.mAngle += self.mAngularSpeed
        
        if abs(self.mAngle) > 359:
            self.mAngle = self.mAngle % 360
            
        if self.mAngle < 0:
            self.mAngle += 360
    
    def getEdge(self):
        return (self.mP.getX() - self.mR, self.mP.getY() - self.mR)

    # Render
    def render(self, aScreen):
        if self.mAngle != self.mDisplayAngle:
            self.mDisplayImg = self.mImg
            #self.mDisplayImg = pygame.transform.rotate(self.mDisplayImg, self.mAngle)
            self.mDisplayImg = pygame.transform.rotozoom(self.mDisplayImg, self.mAngle, 1)
            self.mDisplayAngle = self.mAngle
            rect = self.mDisplayImg.get_rect()
            self.mR = (rect.width + rect.height) // 4
        aScreen.blit(self.mDisplayImg, self.getEdge())

    # Destroy
    def destroy(self):
        Particle.destroy(self)
        self.mImg = None
        self.mImgRect = None
        self.mAngle = None
        self.hitboxRadius = None
        self.mAngularSpeed = None
        self.mAngularAccel = None
        self.mDisplayImg = None
        self.mDisplayAngle = None
        
    @staticmethod
    def CheckHitboxCollision(p1, p2):
        #Max distance
        dm = p1.hitboxRadius + p2.hitboxRadius
        #Cheap check first, real check after
        if abs(p2.mP.x - p1.mP.x) < dm and abs(p2.mP.y - p1.mP.y) < dm:
            dr = abs(p2.mP - p1.mP)
            if dr < dm:
                return True
        return False