class GameObject(object):
    def __init__(self):
        self.state = None
    
    def isDead(self):
        pass
    
    def update(self):
        pass
    
    def destroy(self):
        self.state = None