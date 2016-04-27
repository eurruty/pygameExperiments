import pygame
import random

from api.Hex import Hex
from api.HexNode import HexNode
from api.HexMap import HexMap
from api.Point import Point
from game.GameHex import GameHex

class GameMap(HexMap):
    HEIGHT = 20
    WIDTH = 23
    HEX_SIZE = 24
    ORIGIN = Point(36, 42)
    IMPASSABILITY_FACTOR = 35
    WAYPOINTS = [(1, 1), (HEIGHT - 2, 1), (HEIGHT - 2, WIDTH - 2), (1, WIDTH - 2)]
    SPAWN_LOC = (HEIGHT - 2, 1)
    HOME_LOC = (1, WIDTH - 2)
    
    def __init__(self):
        
        self.height = GameMap.HEIGHT
        self.width = GameMap.WIDTH
        
        #define map
        self.corners = {}
        self.map = [None] * self.height
        for i in range(self.height):
            self.map[i] = [None] * self.width
        
        #fill map
        for i in range(self.height):
            for j in range(self.width):
                first = -(i // 2)
                q = first + j
                r = i
                currHex = GameHex(q, r, 0, 1)
                self.map[i][j] = currHex
                self.corners.update({(q, r):currHex.getCornersStroked(GameMap.ORIGIN, GameMap.HEX_SIZE)})
                
        self.home = self.getHome()
        self.spawn = self.getSpawn()
        
        self.randomizePassability()
        self.path = self.getPath(self.spawn, self.home)
    
    def getSpawn(self):
        return self.map[GameMap.SPAWN_LOC[0]][GameMap.SPAWN_LOC[1]]
    
    def getHome(self):
        return self.map[GameMap.HOME_LOC[0]][GameMap.HOME_LOC[1]]
                
    def getWeight(self, q, r):
        return HexMap.getHex(self, q, r).w
    
    def pixelToHex(self, p):
        h = Hex.pixelToHex(p, GameMap.ORIGIN, GameMap.HEX_SIZE)
        return self.getHex(h.q, h.r)
    
    def getHexCenter(self, h):
        if self.inBounds(h):
            return h.getCenter(GameMap.ORIGIN, GameMap.HEX_SIZE)
    
    def getCornersAsList(self, h):
        if h != None:
            return self.corners[(h.q, h.r)]
        else:
            return None
    
    def isPassable(self, q, r):
        return HexMap.getHex(self, q, r).p == GameHex.PASSABLE
    
    def getDisabledList(self):
        ds = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].p == GameHex.DISABLED:
                    ds.append(self.map[i][j])
        return ds
    
    def getPassableList(self):
        ps = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].p == GameHex.PASSABLE:
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
                coord = (i, j)
                if not coord in GameMap.WAYPOINTS:
                    r = random.randint(0, 100)
                    if r < GameMap.IMPASSABILITY_FACTOR:
                        self.map[i][j].p = -1
                    else:
                        self.map[i][j].p = 0
        
        if not self.waypointsConnected():
            self.randomizePassability()
    
    def waypointsConnected(self):
        wps = self.getWaypoints()
        size = len(wps)
        for i in range(size):
            nextIndex = (i + 1) % size
            if not self.connected(wps[i], wps[nextIndex]):
                return False
        return True
            
    def getWaypoints(self):
        wps = []
        for i in range(len(GameMap.WAYPOINTS)):
            wps.append(self.map[GameMap.WAYPOINTS[i][0]][GameMap.WAYPOINTS[i][1]])
        return wps
    
    def connected(self, a, b):
        if len(self.getPath(a, b)) > 0:
            return True
        else:
            return False
    
    def cost(self, a, b):
        return 1 + self.getWeight(b.h.q, b.h.r) + self.turningCost(a, b)
    
    def printMap(self):
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                currHex = self.map[i][j]
                line += str(currHex.p)
                line += " "
            print(line)
            
    def update(self):
        self.path = self.getPath(self.spawn, self.home)
    
    def render(self, screen):
        ds = self.getDisabledList()
        ps = self.getPassableList()
            
        for i in range(len(ds)):
            currHex = ds[i]
            currHexCorners = self.corners[(currHex.q, currHex.r)]
            pygame.draw.polygon(screen, (0, 0, 0), currHexCorners, 0)
            pygame.draw.aalines(screen, (0, 0, 0), True, currHexCorners, 1)
            
        for i in range(len(ps)):
            currHex = ps[i]
            currHexCorners = self.corners[(currHex.q, currHex.r)]
            pygame.draw.polygon(screen, (255, 255, 255), currHexCorners, 0)
            pygame.draw.aalines(screen, (255, 255, 255), True, currHexCorners, 1)