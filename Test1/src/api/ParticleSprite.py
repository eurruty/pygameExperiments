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
            self.mDisplayImg = pygame.transform.rotate(self.mDisplayImg, self.mAngle)
            self.mDisplayAngle = self.mAngle
            rect = self.mDisplayImg.get_rect()
            self.mR = (rect.width + rect.height) // 4
        aScreen.blit(self.mDisplayImg, self.getEdge())

    # Destroy
    def destroy(self):
        Particle.destroy(self)
        self.mImg = None 
