from api.Vector import Vector
from api.ParticleSprite import ParticleSprite
from game.GameHex import GameHex
from game.GameMap import GameMap
from game.EnemyManager import EnemyManager

class Tower(GameHex):
    
    STATE_IDLE = 0
    STATE_AIM = 1
    STATE_ATK = 2
    
    ON_SIGHT_OFFSET = 2
    
    DEFAULT_RANGE = 100
    DEFAULT_TURN_SPEED = 4
    DEFAULT_TOWER_IMG = "assets/images/tower1.png"
    
    def __init__(self, q, r):
        GameHex.__init__(self, q, r, GameHex.STATE_IMPASSABLE, 0)
        GameMap.inst().setTower(self)
        
        self.center = GameMap.inst().getHexCenter(self)
        self.sprite = ParticleSprite(0, Vector(self.center.x, self.center.y), Vector(0, 0), Vector(0, 0), Tower.DEFAULT_TOWER_IMG)
        self.target = None
        self.angle = 0
        self.angularSpeed = 0
        self.range = Tower.DEFAULT_RANGE
        self.state = Tower.STATE_IDLE
            
    def inRange(self, enemy):
        diff = enemy.mP - self.center
        dx2 = diff.x * diff.x
        dy2 = diff.y * diff.y
        range2 = self.range * self.range
        
        if dx2 + dy2 > range2:
            return False
        else:
            return True
        
    def setTarget(self, enemy):
        self.target = enemy
    
    def onSight(self, enemy):
        if abs(self.angleDiference(enemy)) > Tower.ON_SIGHT_OFFSET:
            return False
        else:
            return True
    
    def aim(self, enemy):
        if self.angleDiference(enemy) > 0:
            self.angularSpeed = Tower.DEFAULT_TURN_SPEED
        else:
            self.angularSpeed = -Tower.DEFAULT_TURN_SPEED
    
    def fire(self):
        pass
    
    def angleDiference(self, enemy):
        enemyDirection = Vector.AngleDegs(self.center, enemy.mP)
        angleDiff = self.angle - enemyDirection
        angleDiff = (angleDiff + 180) % 360 - 180
        return angleDiff
    
    def update(self):
        if self.state == Tower.STATE_IDLE:
            for i in range(len(EnemyManager.inst().mGameObjects)):
                if self.inRange(EnemyManager.inst().mGameObjects[i]):
                    self.setTarget(EnemyManager.inst().mGameObjects[i])
                    break
                
            if self.target != None:
                self.state = Tower.STATE_AIM
                
        if self.target == None:
            self.state = Tower.STATE_IDLE
            
        if self.state == Tower.STATE_AIM:
            if self.inRange(self.target):
                if self.onSight(self.target):
                    self.angularSpeed = 0
                    self.state = Tower.STATE_ATK
                else:
                    self.aim(self.target)
            else:
                self.target = None
                self.state = Tower.STATE_IDLE
        
        if self.state == Tower.STATE_ATK:
            self.fire(self.target)
            self.state = Tower.STATE_AIM
            
    def render(self, screen):
        self.sprite.render(screen)