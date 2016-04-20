import pygame
from api.Point import Point
from api.Hex import Hex
from api.HexMap import HexMap

HEX_X = Hex(1, 0)
HEX_Y = Hex(0, 1)
HEX_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_ORIGIN = (0, 0)
CENTER = Point(0, 0)

isFullscreen = False
screen = None
imgBackground = None
clock = None
salir = False

testHex = Hex(0, 0)

mouseCoord = None

map = HexMap(20,10)
centerCoord = None
hexCenter = None
cornerCoords = None
corners = []


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
    mouseHex = Hex.pixelToHex(Point(p[0], p[1]), CENTER, HEX_SIZE)
    if mouseHex != testHex:
        testHex = mouseHex
        print(testHex)
    
    centerCoord = testHex.getCenter(CENTER, HEX_SIZE)
    corners = testHex.getCornersAsList(CENTER, HEX_SIZE)

def render():
    screen.blit(imgBackground, (0, 0))
    for i in range(len(map.map)):
        for j in range(len(map.map[i])):
            currHexCorners = map.map[i][j].getCornersAsList(CENTER, HEX_SIZE)
            pygame.draw.lines(screen, (255,255,255), True, currHexCorners, 1)
    screen.blit(hexCenter, (centerCoord.x, centerCoord.y))
    pygame.draw.lines(screen, (255,0,0), True, corners, 1)
    pygame.display.flip()
    
def destroy():
    pygame.quit()
    
    
init()

while not salir:

    update()
    render()
        
destroy()