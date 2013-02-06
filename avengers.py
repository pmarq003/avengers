import player
import eventmanager
import level

import pygame
from pygame.locals import *

#initialize pygame lib
pygame.init()

#Frames per second
FPS = 30

#Milliseconds per frame
mSPF = 1000.0/float(FPS)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
bgcolor = 36, 48, 59

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avengers')

logo = pygame.image.load('images/300x300logo.jpg')
logorect = logo.get_rect()
toCenter = 150
logorect.topleft = (SCREEN_WIDTH/2-toCenter,SCREEN_HEIGHT/2-toCenter)

fontObj = pygame.font.Font('freesansbold.ttf', 100)

currLevel = level.Level1()

#Game loop
while True:

    #Start timer and handle events
    milliStart = pygame.time.get_ticks()
    events = pygame.event.get()
    eventmanager.get().handleEvents(events)

    #Update player and enemies positions/current actions
    currLevel.update()

    #Stuff that's gonna get cut out
    msg = currLevel.player.message
    msgSurface = fontObj.render(msg, False, (0,0,0))
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (0,0)

    #Fill the screen, draw level, flip the buffer
    screen.fill(bgcolor)
    screen.blit(msgSurface, msgRect)
    screen.blit(logo, logorect)
    currLevel.draw(screen)
    pygame.display.flip()

    #Stop timer and sleep for remainder of time
    milliEnd = pygame.time.get_ticks()
    leftover = mSPF - (milliEnd - milliStart)
    if leftover > 0: pygame.time.wait(int(leftover))
