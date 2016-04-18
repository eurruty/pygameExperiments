import pygame
from api.Point import Point
from api.Hex import Hex

HEX_X = Hex(1, 0)
HEX_Y = Hex(0, 1)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_ORIGIN = (0, 0)
CENTER = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

isFullscreen = False
screen = None
imgBackground = None
clock = None
salir = False

testHex = Hex(0, 0)

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
    
    hexCenter = pygame.Surface((3, 3))
    hexCenter = hexCenter.convert()
    hexCenter.fill((0, 255, 0))
    
    clock = pygame.time.Clock()
    
def update():
    global salir
    global screen
    global isFullscreen
    global testHex
    global centerCoord
    global cornerCoords
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
                    
            if event.key == pygame.K_UP:
                testHex.substract(HEX_Y)
            if event.key == pygame.K_DOWN:
                testHex.add(HEX_Y)
            if event.key == pygame.K_LEFT:
                testHex.substract(HEX_X)
            if event.key == pygame.K_RIGHT:
                testHex.add(HEX_X)
    
    print(testHex)
    centerCoord = testHex.getCenter(CENTER, 30)
    cornerCoords = testHex.getCorners(CENTER, 30)
    corners = []
    for x in range(len(cornerCoords)):
        corners.append(pygame.Surface((3, 3)))
        corners[x] = corners[x].convert()
        corners[x].fill((255, 0, 0))

def render():
    screen.blit(imgBackground, (0, 0))
    screen.blit(hexCenter, (centerCoord.x, centerCoord.y))
    for x in range(len(corners)):
        screen.blit(corners[x], (cornerCoords[x].x, cornerCoords[x].y))
    pygame.display.flip()
    
def destroy():
    pygame.quit()
    
    
init()

while not salir:

    update()
    render()
        
destroy()