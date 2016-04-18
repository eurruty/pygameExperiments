class Point(object):
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __str__(self):
        return ("[" + str(self.x) + ", " + str(self.y) + "]")
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented
        
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented
        
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
    
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5