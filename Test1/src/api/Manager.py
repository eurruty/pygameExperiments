class Manager(object):
    mInstance = None
    mInitialized = False
    
    mGameObjects = None
    
    def __new__(self, *args, **kargs):
        if (Manager.mInstance is None):
            Manager.mInstance = object.__new__(self, *args, **kargs)
            self.init(Manager.mInstance)
        return self.mInstance
    
    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (Manager.mInitialized):
            return
        Manager.mInitialized = True
        Manager.mGameObjects = []
    
    def update(self):
        for gameObject in Manager.mGameObjects:
            gameObject.update()
    
    def render(self, aScreen):
        for gameObject in Manager.mGameObjects:
            gameObject.render(aScreen)
    
    def add(self, aGameObject):
        Manager.mGameObjects.append(aGameObject)
        
    def destroy(self):
        Manager.mInstance = None