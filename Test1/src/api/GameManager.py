class GameManager(object):
    mInstance = None
    mInitialized = False
    
    mGameObjects = None
    
    def __new__(self, *args, **kargs):
        if (GameManager.mInstance is None):
            GameManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(GameManager.mInstance)
        return self.mInstance
    
    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (GameManager.mInitialized):
            return
        GameManager.mInitialized = True
        GameManager.mGameObjects = []
    
    def update(self):
        for o in GameManager.mGameObjects:
            o.update()
    
    def render(self, aScreen):
        for o in GameManager.mGameObjects:
            o.render(aScreen)
    
    def add(self, aGameObject):
        GameManager.mGameObjects.append(aGameObject)
        
    def destroy(self):
        GameManager.mInstance = None