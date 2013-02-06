import os, sys

from player import CaptainAmerica
from eventmanager import EventManager

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
#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avengers')
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255
black = 0, 0, 0
bgcolor = 36, 48, 59
screen.fill(bgcolor)

logo = pygame.image.load('300x300logo.jpg')
logorect = logo.get_rect()
toCenter = 150
logorect.topleft = (SCREEN_WIDTH/2-toCenter,SCREEN_HEIGHT/2-toCenter)

player1 = CaptainAmerica(SCREEN_HEIGHT - 100)

fontObj = pygame.font.Font('freesansbold.ttf', 100)
msg = 'Avengers'

evman = EventManager()

while True:
    milliStart = pygame.time.get_ticks()

    evman.handleEvents(pygame.event.get())
    player1.update(evman)

    msg = player1.message
    msgSurface = fontObj.render(msg, False, black)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (0,0)

    screen.fill(bgcolor)
    screen.blit(msgSurface, msgRect)
    screen.blit(logo, logorect)
    screen.blit(player1.image, player1.position)
    pygame.display.flip()

    milliEnd = pygame.time.get_ticks()
    leftover = mSPF - (milliEnd - milliStart)
    if leftover > 0: pygame.time.wait(int(leftover))

clock.tick(30)
