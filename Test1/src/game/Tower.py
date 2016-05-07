import pygame

from api.Vector import Vector
from api.ParticleSprite import ParticleSprite
from game.GameHex import GameHex
from game.GameMap import GameMap
from game.EnemyManager import EnemyManager
from game.HomingProjectile import HomingProjectile
from game.ProjectileManager import ProjectileManager

class Tower(GameHex):
    
    STATE_IDLE = 0
    STATE_AIM = 1
    STATE_ATK = 2
    
    ON_SIGHT_OFFSET = 1
    
    DEFAULT_RANGE = GameMap.HEX_SIZE * 6
    DEFAULT_TURN_SPEED = 4
    DEFAULT_TOWER_IMG = "assets/images/tower1.png"
    DEFAULT_COOLDOWN = 10
    
    def __init__(self, q, r):
        GameHex.__init__(self, q, r, GameHex.STATE_IMPASSABLE, 0)
        GameMap.inst().setTower(self)
        
        self.center = GameMap.inst().getHexCenter(self)
        self.sprite = ParticleSprite(0, Vector(self.center.x, self.center.y), Vector(0, 0), Vector(0, 0), Tower.DEFAULT_TOWER_IMG)
        self.target = None
        self.cooldown = 0
        self.sprite.mAngle = 0
        self.sprite.mAngularSpeed = 0
        self.range = Tower.DEFAULT_RANGE
        self.range2 = self.range * self.range
        self.towerState = Tower.STATE_IDLE
            
    def inRange(self, enemy):
        if self.distance2(enemy) > self.range2:
            return False
        else:
            return True
    
    def distance2(self, enemy):
        diff = enemy.mP - self.center
        dx2 = diff.x * diff.x
        dy2 = diff.y * diff.y
        return dx2 + dy2
        
    def setTarget(self, enemy):
        self.target = enemy
    
    def onSight(self):
        if abs(self.angleDiference()) > Tower.ON_SIGHT_OFFSET:
            return False
        else:
            return True
    
    def aim(self):
        if self.angleDiference() > 0:
            self.sprite.mAngularSpeed = Tower.DEFAULT_TURN_SPEED
        else:
            self.sprite.mAngularSpeed = -Tower.DEFAULT_TURN_SPEED
    
    def fire(self):
        if self.cooldown == 0:
            ProjectileManager.inst().addProjectile(HomingProjectile(self, self.target))
            self.cooldown = Tower.DEFAULT_COOLDOWN
    
    def angleDiference(self):
        diff = self.center - self.target.mP
        enemyDirection = diff.getAngleDegs()
        angleDiff = enemyDirection - self.sprite.mAngle
        angleDiff = (angleDiff + 180) % 360 - 180
        return angleDiff
    
    def update(self):
        self.sprite.update()
        
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.towerState == Tower.STATE_IDLE:
            
            target = None
            distance = None
            
            for i in range(len(EnemyManager.inst().mArray)):
                
                currTarget = EnemyManager.inst().mArray[i]
                currDistance = self.distance2(currTarget)
                
                if currDistance <= self.range2:
                    if target == None:
                        target = currTarget
                        distance = currDistance
                    else:
                        if currDistance < distance:
                            target = currTarget
                            distance = currDistance
                            
            if target != None:
                self.setTarget(target)
                self.towerState = Tower.STATE_AIM
                
                
        if self.target == None:
            self.sprite.mAngularSpeed = 0
            self.towerState = Tower.STATE_IDLE
            
        if self.towerState == Tower.STATE_AIM:
            if self.inRange(self.target):
                if self.onSight():
                    self.sprite.mAngularSpeed = 0
                    self.towerState = Tower.STATE_ATK
                else:
                    self.aim()
            else:
                self.target = None
                self.sprite.mAngularSpeed = 0
                self.towerState = Tower.STATE_IDLE
        
        if self.towerState == Tower.STATE_ATK:
            self.fire()
            self.towerState = Tower.STATE_AIM

    def render(self, screen):
        self.sprite.render(screen)
        
        #debug target
        if self.target != None:
            pygame.draw.aalines(screen, (255, 0, 0), False, ((self.center.x, self.center.y), (self.target.mP.x, self.target.mP.y)), 1)