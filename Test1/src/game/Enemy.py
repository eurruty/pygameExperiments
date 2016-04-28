from api.ParticleSprite import ParticleSprite
from api.Vector import Vector

class Enemy(ParticleSprite):
    IMG_PATH = "assets/images/tri.png"
    def __init__(self, x, y):
        ParticleSprite.__init__(self, 1, Vector(x, y), Vector(0, 0), Vector(0, 0), Enemy.IMG_PATH)