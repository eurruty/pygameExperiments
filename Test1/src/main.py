import pygame
from api.Point import Point
from api.Hex import Hex
#from api.HexMap import HexMap
from game.GameMap import GameMap

HEX_X = Hex(1, 0)
HEX_Y = Hex(0, 1)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_ORIGIN = (0, 0)
CENTER = Point(36, 42)

isFullscreen = False
screen = None
imgBackground = None
clock = None
salir = False

testHex = Hex(0, 0)

mouseCoord = None

hexMap = GameMap()
hexMap.printMap()
centerCoord = None
hexCenter = None
cornerCoords = None
corners = []
path = []


def init():
    global screen
    global imgBackground
    global imgPutin
    global corners
    global clock
    global hexCenter
    
    pygame.init()

    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Test1")

    imgBackground = pygame.Surface(screen.get_size())
    imgBackground = imgBackground.convert()
    
    imgPutin = pygame.image.load("assets/images/putin.jpg")
    imgPutin = imgPutin.convert()
    imgPutin = pygame.transform.smoothscale(imgPutin, RESOLUTION)

    imgBackground.blit(imgPutin, SCREEN_ORIGIN)
    
    hexCenter = pygame.Surface((1, 1))
    hexCenter = hexCenter.convert()
    hexCenter.fill((255, 0, 0))
    
    clock = pygame.time.Clock()
    
def update():
    global salir
    global screen
    global isFullscreen
    global testHex
    global mouseCoord
    global centerCoord
    global corners
    global path

    clock.tick(60)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            salir = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                isFullscreen = not isFullscreen
                if isFullscreen:
                    screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(RESOLUTION)
    
    p = pygame.mouse.get_pos()
    mouseHex = hexMap.pixelToHex(Point(p[0], p[1]))
    if mouseHex != testHex:
        testHex = mouseHex
        centerCoord = hexMap.getHexCenter(testHex)
        corners = hexMap.getCornersAsList(testHex)
        path = hexMap.getPath(hexMap.spawn, mouseHex)

def render():
    screen.blit(imgBackground, (0, 0))
    
    hexMap.render(screen)
    
    for i in range(len(path)):
        currHexCorners = hexMap.getCornersAsList(path[i])
        pygame.draw.polygon(screen, (0, 0, 255), currHexCorners, 0)
        pygame.draw.aalines(screen, (0, 0, 255), True, currHexCorners, 1)
        
    if centerCoord != None and corners != None:
        screen.blit(hexCenter, (centerCoord.x, centerCoord.y))
        pygame.draw.aalines(screen, (255, 0, 0), True, corners, 1)
        
    pygame.display.flip()
    
def destroy():
    pygame.quit()
    
init()

while not salir:

    update()
    render()
        
destroy()