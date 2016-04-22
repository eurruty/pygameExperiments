from Hex import Hex
from HexNode import HexNode
from PriorityQueue import PriorityQueue

class HexMap(object):
    TURNING_COST = [0.00, 0.33, 0.66, 1.00, 0.66, 0.33]
    
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
    
    def getNeighborNodes(self, h):
        nNodes = []
        for i in range(0, 6):
            nHex = h.getNeighbor(i)
            if self.inBounds(nHex):
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
                newCost = currCost[currNode] + HexMap.cost(currNode, nextNode)
                if nextNode not in currCost or newCost < currCost[nextNode]:
                    currCost[nextNode] = newCost
                    priority = newCost + HexMap.heuristic(goalNode, nextNode)
                    frontier.put(nextNode, priority)
                    cameFrom[nextNode] = currNode
        
        return cameFrom, currCost
    
    def getPath(self, startHex, goalHex):
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
        
        path = []
        
        if endNode != None:
            path.append(endNode.h)
            currNode = s[0][endNode]
            if currNode != None:
                while currNode.h != startHex:
                    path.append(currNode.h)
                    currNode = s[0][currNode]
                path.append(startHex)
        
        return path
    
    @staticmethod
    def heuristic(a, b):
        return a.h.getDistance(b.h)
        
    @staticmethod
    def cost(a, b):
        return 1 + HexMap.turningCost(a, b)
    
    @staticmethod
    def turningCost(a, b):
        if a.d == None or b.d == None:
            return 0
        else:
            diff = abs(a.d - b.d)
            return HexMap.TURNING_COST[diff]
        