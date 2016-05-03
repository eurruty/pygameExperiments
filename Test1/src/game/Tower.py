from game.GameHex import GameHex

class Tower(GameHex):
    
    STATE_IDLE = 0
    STATE_AIM = 1
    STATE_ATK = 2
    
    def __init__(self, q, r):
        GameHex.__init__(self, q, r, GameHex.STATE_IMPASSABLE, 0)
        self.targetList = []
        self.target = None
        self.state = Tower.STATE_IDLE
        
    def update(self):
        if self.state == Tower.STATE_IDLE:
            for i in range(len(self.targetList)):
                if self.inRange(self.targetList[i]):
                    self.target = self.targetList[i]
                    break
                
            if self.target != None:
                self.state = Tower.STATE_AIM
                
        if self.target == None:
            self.state = Tower.STATE_IDLE
            
        if self.state == Tower.STATE_AIM:
            if self.inRange():
                self.aim()
            if self.onSight():
                self.state = Tower.STATE_ATK
        
        if self.state == Tower.STATE_ATK:
            self.fire()
            self.state = Tower.STATE_AIM
            
    def inRange(self):
        pass
    
    def onSight(self):
        pass
    
    def aim(self):
        pass
    
    def fire(self):
        pass
        