from Hex import Hex
from PriorityQueue import PriorityQueue

class HexMap(object):
    def __init__(self, height, width):
        
        self.height = height
        self.width = width
        
        #define map
        self.map = [None] * height
        for i in range(height):
            self.map[i] = [None] * width
        
        #fill map
        for i in range(height):
            for j in range(width):
                first = -(i // 2)
                q = first + j
                r = i
                self.map[i][j] = Hex(q, r)
    
    def getHex(self, q, r):
        x = q - (r // 2)
        y = r
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[x][y]
        else:
            return None
    
    def setHex(self, h):
        if self.inBounds(h):
            x = h.q + (h.r // 2)
            y = h.r
            self.map[x][y] = h
    
    def getList(self):
        hexList = ()
        for i in range(self.map):
            for j in range(self.map[i]):
                hexList.append(self.map[i][j])
        return hexList
    
    def inBounds(self, h):
        return 0 <= (h.q + (h.r // 2)) < self.width and 0 <= h.r < self.height
    
    def search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for n in current.getNeighbors():
                if self.inBounds(n):
                    new_cost = cost_so_far[current] + HexMap.cost(current, n)
                    if n not in cost_so_far or new_cost < cost_so_far[n]:
                        cost_so_far[n] = new_cost
                        priority = new_cost + HexMap.heuristic(goal, n)
                        frontier.put(n, priority)
                        came_from[n] = current
        
        return came_from, cost_so_far
    
    @staticmethod
    def heuristic(a, b):
        return a.getDistance(b)
    
    @staticmethod
    def cost(a, b):
        return 1