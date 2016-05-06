class Manager(object):

    def __init__(self):
        
        self.mArray = []

    def update(self):
        for e in self.mArray:
            e.update()

        i = len(self.mArray)
        while i > 0:
            if self.mArray[i - 1].isDead():
                self.mArray[i - 1].destroy()
                self.mArray.pop(i - 1)
            i = i - 1

    def render(self, aScreen):
        for e in self.mArray:
            e.render(aScreen)

    def add(self, aElement):
        self.mArray.append(aElement)
        
    def getLength(self):
        return len(self.mArray)

    def destroy(self):
        i = len(self.mArray)
        while i > 0:
            self.mArray[i - 1].destroy()
            self.mArray.pop(i - 1)
            i = i - 1
