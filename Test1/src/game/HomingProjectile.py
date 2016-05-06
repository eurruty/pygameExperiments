from api.ParticleSprite import ParticleSprite
from api.Vector import Vector

class HomingProjectile(ParticleSprite):
    
    IMG_PATH = "assets/images/proj.png"
    DEFAULT_SPEED = 4
    DEFAULT_OFFSET = Vector(4, 0)
    
    def __init__(self, source, target, offset=DEFAULT_OFFSET):
        
        direction = source.center - target.mP 
        angle = direction.getAngleDegs()
        position = source.center
        
        if offset != None:
            rOffset = offset
            rOffset.rotateDegs(angle)
            rOffset.y = -rOffset.y
            position += rOffset
            
        speed = Vector(HomingProjectile.DEFAULT_SPEED, 0)
        speed.rotateDegs(angle)
        speed.y = -speed.y
        
        ParticleSprite.__init__(self, 0, position, speed, Vector(0, 0), HomingProjectile.IMG_PATH)
        
        self.mAngle = angle