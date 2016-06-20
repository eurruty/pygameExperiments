from api.ParticleSprite import ParticleSprite
from api.Vector import Vector
from game.GameMap import GameMap

class HomingProjectile(ParticleSprite):
    
    IMG_PATH = "assets/images/proj.png"
    DEFAULT_SPEED = 4
    DEFAULT_TTL = ((GameMap.HEX_SIZE * 6) // DEFAULT_SPEED) + 10
    DEFAULT_OFFSET = Vector(32, 0)
    DEFAULT_HITBOX_RADIUS = 2
    DEFAULT_DAMAGE = 5
    
    def __init__(self, source, target, offset=DEFAULT_OFFSET):
        
        direction = source.center - target.mP 
        angle = direction.getAngleDegs()
        position = source.center
        if offset != None:
            rOffset = offset
            rOffset.setAngleDegs(angle)
            rOffset.y = -rOffset.y
            position += rOffset
            
        speed = Vector(HomingProjectile.DEFAULT_SPEED, 0)
        speed.rotateDegs(angle)
        speed.y = -speed.y
        
        ParticleSprite.__init__(self, 0, position, speed, Vector(0, 0), HomingProjectile.IMG_PATH)
        
        self.hitboxRadius = HomingProjectile.DEFAULT_HITBOX_RADIUS
        self.target = target
        self.mAngle = angle
        self.live = True
        self.time = 0
        
    def isDead(self):
        return not self.live
    
    def updateDirection(self):
        diff = self.mP - self.target.mP
        
        enemyDirection = diff.getAngleDegs()
        
        self.mAngle = enemyDirection
        
        self.mS.x = HomingProjectile.DEFAULT_SPEED
        self.mS.y = 0
        self.mS.setAngleDegs(enemyDirection)
        self.mS.y = -self.mS.y
        
    def update(self):
        self.time += 1
        if self.time > HomingProjectile.DEFAULT_TTL:
            self.live = False
            
        if not self.target.isDead():
            self.updateDirection()
            if ParticleSprite.CheckHitboxCollision(self, self.target):
                self.target.hp -= HomingProjectile.DEFAULT_DAMAGE
                self.live = False
        
        ParticleSprite.update(self)
            
    def render(self, screen):
        ParticleSprite.render(self, screen)
        
    def destroy(self):
        ParticleSprite.destroy(self)
        self.target = None
        self.mAngle = None
        self.live = None
        self.time = None