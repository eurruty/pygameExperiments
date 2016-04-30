from api.ParticleSprite import ParticleSprite
from api.Vector import Vector

class Enemy(ParticleSprite):
    IMG_PATH = "assets/images/tri.png"
    ANGLES = [0, 60, 120, 180, 240, 300]
    SPEED_FACTOR = 8
    
    STATE_ADVANCE = 0
    STATE_RETREAT = 1
    STATE_SWITCH_STEP = 2
    STATE_DIE = 3
    
    STATES = [STATE_ADVANCE, STATE_RETREAT, STATE_SWITCH_STEP, STATE_DIE]
    
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.steps = len(self.waypoints)
        
        ParticleSprite.__init__(self, 1, Vector(self.waypoints[0][0].x, self.waypoints[0][0].y), Vector(0, 0), Vector(0, 0), Enemy.IMG_PATH)
        
        self.currStep = 0
        self.currStepAdvance = 0
        self.currStepStart = self.waypoints[self.currStep][0]
        self.currStepEnd = self.waypoints[self.currStep][1]
        self.currStepDiff = self.currStepEnd - self.currStepStart
        self.currStepMoveX = self.currStepDiff.x / 100.0
        self.currStepMoveY = self.currStepDiff.y / 100.0
        self.currStepAngle = Enemy.ANGLES[self.waypoints[0][2]]
        
        self.mAngle = self.currStepAngle
        
        self.state = Enemy.STATE_ADVANCE
        
    def newStepAdv(self):
        self.currStep += 1
        if self.currStep >= self.steps:
            self.state = Enemy.STATE_RETREAT
            self.currStep = self.steps
            self.newStepRet()
        else:
            self.currStepAdvance = 0
            self.currStepStart = self.waypoints[self.currStep][0]
            self.currStepEnd = self.waypoints[self.currStep][1]
            self.currStepDiff = self.currStepEnd - self.currStepStart
            self.currStepMoveX = self.currStepDiff.x / 100.0
            self.currStepMoveY = self.currStepDiff.y / 100.0
            self.currStepAngle = Enemy.ANGLES[self.waypoints[self.currStep][2]]
            self.currStepAngleDiff = self.currStepAngle - self.mAngle
            
    def newStepRet(self):
        self.currStep -= 1
        if self.currStep < 0:
            self.state = Enemy.STATE_ADVANCE
            self.currStep = -1
            self.newStepAdv()
        else:
            self.currStepAdvance = 0
            self.currStepStart = self.waypoints[self.currStep][0]
            self.currStepEnd = self.waypoints[self.currStep][1]
            self.currStepDiff = self.currStepEnd - self.currStepStart
            self.currStepMoveX = self.currStepDiff.x / 100.0
            self.currStepMoveY = self.currStepDiff.y / 100.0
            self.currStepAngle = Enemy.ANGLES[(self.waypoints[self.currStep][2] + 3) % 6]
            self.currStepAngleDiff = self.currStepAngle - self.mAngle
                    
    def turn(self):
        angularSpeed = Enemy.SPEED_FACTOR * 2
        angleModifier = None
        if self.currStepAngleDiff > 0:
            angleModifier = angularSpeed
        else:
            angleModifier = -angularSpeed
         
        if abs(self.currStepAngleDiff) > 180:
            angleModifier = -angleModifier
             
        self.mAngle += angleModifier
         
        if abs(self.mAngle) > 359:
            self.mAngle = self.mAngle % 360
             
        if self.mAngle < 0:
            self.mAngle += 360
        
        if abs(self.currStepAngle - self.mAngle) <= ((angularSpeed + 1) // 2) or abs(self.currStepAngle - self.mAngle) >= 360 - ((angularSpeed + 1) // 2):
            self.mAngle = self.currStepAngle
        
    def advance(self):
        if self.mAngle != self.currStepAngle:
            self.turn()
        else:
            self.currStepAdvance += Enemy.SPEED_FACTOR
            if self.currStepAdvance < 100:
                x = self.currStepStart.x + (self.currStepMoveX * self.currStepAdvance)
                y = self.currStepStart.y + (self.currStepMoveY * self.currStepAdvance)
                self.mP = Vector(x, y)
            else:
                self.mP = Vector(self.currStepEnd.x, self.currStepEnd.y)
                self.newStepAdv()
            
    def retreat(self):
        if self.mAngle != self.currStepAngle:
            self.turn()
        else:
            self.currStepAdvance += Enemy.SPEED_FACTOR
            if self.currStepAdvance < 100:
                x = self.currStepEnd.x - (self.currStepMoveX * self.currStepAdvance)
                y = self.currStepEnd.y - (self.currStepMoveY * self.currStepAdvance)
                self.mP = Vector(x, y)
            else:
                self.mP = Vector(self.currStepStart.x, self.currStepStart.y)
                self.newStepRet()
        
        
    def update(self):
        if self.state != None:
                
            if self.state == Enemy.STATE_ADVANCE:
                self.advance()
                    
            if self.state == Enemy.STATE_RETREAT:
                self.retreat()
            
            if self.state == Enemy.STATE_DIE:
                self.destroy()
                
        ParticleSprite.update(self)