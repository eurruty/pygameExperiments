import pygame
import random

from api.HexNode import HexNode
from api.HexMap import HexMap
from game.GameHex import GameHex

class GameMap(HexMap):
    def __init__(self, height, width, dPass, dWeight, hSize, center):
        self.height = height
        self.width = width
        self.hSize = hSize
        self.center = center
        
        #define map
        self.corners = {}
        self.map = [None] * height
        for i in range(height):
            self.map[i] = [None] * width
        
        #fill map
        for i in range(height):
            for j in range(width):
                first = -(i // 2)
                q = first + j
                r = i
                currHex = GameHex(q, r, dPass, dWeight)
                self.map[i][j] = currHex
                self.corners.update({(q, r):currHex.getCornersStroked(self.center, self.hSize)})
                
    def getWeight(self, q, r):
        return HexMap.getHex(self, q, r).w
    
    def getCornersAsList(self, h):
        return self.corners[(h.q, h.r)]
    
    def isPassable(self, q, r):
        res = HexMap.getHex(self, q, r).p
        return res
    
    def getImpassableList(self):
        ip = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not self.map[i][j].p:
                    ip.append(self.map[i][j])
        return ip
    
    def getPassableList(self):
        ps = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].p:
                    ps.append(self.map[i][j])
        return ps
    
    def getPassableNeighbors(self, h):
        ns = ()
        for i in range(0, 6):
            nHex = self.getNeighbor(h, i)
            if nHex != None and self.isPassable(nHex.q, nHex.r):
                ns.append(nHex)
        return ns
    
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
    
    def render(self, screen):
        ip = self.getImpassableList()
        ps = self.getPassableList()
            
        for i in range(len(ip)):
            currHex = ip[i]
            currHexCorners = self.corners[(currHex.q, currHex.r)]
            pygame.draw.polygon(screen, (0, 0, 0), currHexCorners, 0)
            pygame.draw.aalines(screen, (0, 0, 0), True, currHexCorners, 1)
            
        for i in range(len(ps)):
            currHex = ps[i]
            currHexCorners = self.corners[(currHex.q, currHex.r)]
            pygame.draw.polygon(screen, (255, 255, 255), currHexCorners, 0)
            pygame.draw.aalines(screen, (255, 255, 255), True, currHexCorners, 1)