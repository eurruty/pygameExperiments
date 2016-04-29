from Hex import Hex
from HexNode import HexNode
from PriorityQueue import PriorityQueue

class HexMap(object):
    #CLOCK[  3 ]  [  1  ]  [  11 ]  [  9  ]  [  7  ]  [  5 ]
    DR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    
    #CLOCK[  2  ]  [  12 ]  [  10  ]  [  8  ]  [  6  ]  [  4 ]
    DG = [(2, -1), (1, -2), (-1, -1), (-2, 1), (-1, 2), (1, 1)]
    
    #ANGLE         [  0] [ 60] [120] [180] [120] [ 60]
    TURNING_COST = [0.00, 0.50, 1.00, 1.50, 1.00, 0.50]
    
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
        i = r
        j = q + (r // 2)
        if 0 <= j < self.width and 0 <= i < self.height:
            return self.map[i][j]
        else:
            return None
    
    def setHex(self, h):
        if self.inBounds(h):
            i = h.r
            j = h.q + (h.r // 2)
            self.map[i][j] = h
    
    def getList(self):
        hexList = ()
        for i in range(self.map):
            for j in range(self.map[i]):
                hexList.append(self.map[i][j])
        return hexList
    
    def inBounds(self, h):
        if h != None:
            return 0 <= (h.q + (h.r // 2)) < self.width and 0 <= h.r < self.height
        else:
            return False
    
    def rotate60(self, center, h):
        q = center.q - (h.s - center.s)
        r = center.r - (h.q - center.q)
        return self.getHex(q, r)
    
    def getNeighbor(self, h, d):
        q = h.q + HexMap.DR[d][0]
        r = h.r + HexMap.DR[d][1]
        return self.getHex(q, r)
    
    def getNeighbors(self, h):
        n = ()
        for i in range(0, 6):
            q = h.q + HexMap.DR[i][0]
            r = h.r + HexMap.DR[i][1]
            n.append(self.getHex(q, r))
        return n
    
    def getDiagNeighbor(self, h, d):
        q = h.q + HexMap.DG[d][0]
        r = h.r + HexMap.DG[d][1]
        return self.getHex(q, r)
    
    def getNeighborNodes(self, h):
        nNodes = []
        for i in range(0, 6):
            nHex = self.getNeighbor(h, i)
            if nHex != None:
                nNode = HexNode(nHex, i)
                nNodes.append(nNode)
        return nNodes
    
    def search(self, startHex, goalHex):
        startNode = HexNode(startHex, None)
        goalNode = HexNode(goalHex, None)
        frontier = PriorityQueue()
        frontier.put(startNode, 0)
        cameFrom = {}
        currCost = {}
        cameFrom[startNode] = None
        currCost[startNode] = 0
        
        while not frontier.empty():
            currNode = frontier.get()
            
            if currNode.h == goalNode.h:
                break
            
            for nextNode in self.getNeighborNodes(currNode.h):
                newCost = currCost[currNode] + self.cost(currNode, nextNode)
                if nextNode not in currCost or newCost < currCost[nextNode]:
                    currCost[nextNode] = newCost
                    priority = newCost + HexMap.heuristic(goalNode, nextNode)
                    frontier.put(nextNode, priority)
                    cameFrom[nextNode] = currNode
        
        return cameFrom, currCost
    
    def getPath(self, startHex, goalHex):
        path = []
        if startHex != None and goalHex != None:
            s = self.search(startHex, goalHex)
            endNode = None
            cost = None
            for hexNode in s[0]:
                if hexNode.h == goalHex:
                    if endNode == None:
                        endNode = hexNode
                        cost = s[1][hexNode]
                    elif cost > s[1][hexNode]:
                        endNode = hexNode
                        cost = s[1][hexNode]
            
            if endNode != None:
                path.append(endNode.h)
                currNode = s[0][endNode]
                if currNode != None:
                    while currNode.h != startHex:
                        path.append(currNode.h)
                        currNode = s[0][currNode]
                    path.append(startHex)
        
        return path
    
    def cost(self, a, b):
        return 1 + self.turningCost(a, b)
    
    def turningCost(self, a, b):
        if a.d == None or b.d == None:
            return 0
        else:
            diff = abs(a.d - b.d)
            return HexMap.TURNING_COST[diff]
        
    @staticmethod
    def direction(a, b):
        diff = (b - a).getAxialCoords()
        if diff in HexMap.DR:
            return HexMap.DR.index(diff)
        else:
            return None
    
    @staticmethod
    def distance(a, b):
        if a != None and b != None:
            return (abs(b.q - a.q) + abs(b.r - a.r) + abs(b.s - a.s)) // 2
        else:
            return None
    
    @staticmethod
    def heuristic(a, b):
        return HexMap.distance(a.h, b.h)
        