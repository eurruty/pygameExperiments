from api.ParticleSprite import ParticleSprite
from api.Vector import Vector

class Enemy(ParticleSprite):
    IMG_PATH = "assets/images/tri.png"
    ANGLES = [0, 60, 120, 180, 240, 300]
    SPEED_FACTOR = 8
    
    STATE_ADVANCE = 0
    STATE_RETURN = 1
    STATE_SWITCH_STEP = 2
    STATE_DIE = 3
    
    STATES = [STATE_ADVANCE, STATE_RETURN, STATE_SWITCH_STEP, STATE_DIE]
    
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
        
    def newStep(self):
        if self.currStep < 0:
            self.currStep = 0
            self.state = Enemy.STATE_ADVANCE
        if self.currStep >= self.steps:
            self.currStep = self.steps - 1
            self.state = Enemy.STATE_RETURN
        self.currStepAdvance = 0
        self.currStepStart = self.waypoints[self.currStep][0]
        self.currStepEnd = self.waypoints[self.currStep][1]
        self.currStepDiff = self.currStepEnd - self.currStepStart
        self.currStepMoveX = self.currStepDiff.x / 100.0
        self.currStepMoveY = self.currStepDiff.y / 100.0
        #self.currStepAngle = Enemy.ANGLES[self.waypoints[0][2]]
        #self.currStepAngleDiff = (self.currStepAngle - self.mAngle) % 180
        
        
        
    def update(self):
        if self.state != None:
                
            if self.state == Enemy.STATE_ADVANCE:
                self.currStepAdvance += Enemy.SPEED_FACTOR
                if self.currStepAdvance < 100:
                    x = self.currStepStart.x + (self.currStepMoveX * self.currStepAdvance)
                    y = self.currStepStart.y + (self.currStepMoveY * self.currStepAdvance)
                    self.mP = Vector(x, y)
                else:
                    self.mP = Vector(self.currStepEnd.x, self.currStepEnd.y)
                    self.currStep += 1
                    self.newStep()
                    
            if self.state == Enemy.STATE_RETURN:
                self.currStepAdvance += Enemy.SPEED_FACTOR
                if self.currStepAdvance < 100:
                    x = self.currStepEnd.x - (self.currStepMoveX * self.currStepAdvance)
                    y = self.currStepEnd.y - (self.currStepMoveY * self.currStepAdvance)
                    self.mP = Vector(x, y)
                else:
                    self.mP = Vector(self.currStepStart.x, self.currStepStart.y)
                    self.currStep -= 1
                    self.newStep()
            
            if self.state == Enemy.STATE_DIE:
                self.destroy()