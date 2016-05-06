from api.Manager import Manager

class TowerManager(Manager):
    
    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (TowerManager.mInstance is None):
            TowerManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(TowerManager.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (TowerManager.mInitialized):
            return
        TowerManager.mInitialized = True

        Manager.__init__(self)

    def update(self):
        Manager.update(self)

    def render(self, aScreen):
        Manager.render(self, aScreen)

    def addTower(self, aTower):
        Manager.add(self, aTower)
      
    def destroy(self):
        Manager.destroy(self)
        
        TowerManager.mInstance = None