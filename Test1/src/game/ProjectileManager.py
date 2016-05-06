from api.Manager import Manager

class ProjectileManager(Manager):
    
    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (ProjectileManager.mInstance is None):
            ProjectileManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(ProjectileManager.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (ProjectileManager.mInitialized):
            return
        ProjectileManager.mInitialized = True

        Manager.__init__(self)

    def update(self):
        Manager.update(self)

    def render(self, aScreen):
        Manager.render(self, aScreen)

    def addProjectile(self, aProjectile):
        Manager.add(self, aProjectile)
      
    def destroy(self):
        Manager.destroy(self)
        
        ProjectileManager.mInstance = None