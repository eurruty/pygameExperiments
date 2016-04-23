import random
from api.HexNode import HexNode
from api.HexMap import HexMap
from game.GameHex import GameHex

class GameMap(HexMap):
    def __init__(self, height, width, dPass, dWeight):
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
                self.map[i][j] = GameHex(q, r, dPass, dWeight)
                
    def getWeight(self, q, r):
        return HexMap.getHex(self, q, r).w
    
    def isPassable(self, q, r):
        res = HexMap.getHex(self, q, r).p
        return res
    
    def getNeighborNodes(self, h):
        nNodes = []
        for i in range(0, 6):
            nHex = self.getNeighbor(h, i)
            if nHex != None and self.isPassable(nHex.q, nHex.r):
                nNode = HexNode(nHex, i)
                nNodes.append(nNode)
        return nNodes
    
    def randomizePassability(self):
        for i in range(self.height):
            for j in range(self.width):
                r = random.randint(0,3)
                if r == 2:
                    self.map[i][j].p = False
    
    def cost(self, a, b):
        return 1 + self.getWeight(b.h.q, b.h.r) + self.turningCost(a, b)
    
    def printMap(self):
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                currHex = self.map[i][j]
                if currHex.p:
                    line += str(currHex.w)
                else:
                    line += "X"
                line += " "
            print(line)