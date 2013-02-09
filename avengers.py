#testing git commit lol

import camera
import constants
import eventmanager
import image
import level
import player
import pygame
import time

from constants import SCREEN_WIDTH,SCREEN_HEIGHT
from pygame.locals import *

#initialize pygame lib
pygame.init()

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Avengers - Six Guys')

#splash screen
splash = pygame.Surface(screen.get_size())
splash = splash.convert()
splash.fill((0,0,0))
x, y = screen.get_size()
screen.blit(splash, (0, 0))
logo = pygame.image.load("images/300x300logo.jpg").convert_alpha()
screen.blit(logo, (0,0))
pygame.display.update()
time.sleep(2)

#Make a camera (this might need to go inside the level object, but that's ok)
camera = camera.Camera(screen)

currLevel = level.Level1()

#Game loop
while True:

    #Start timer and handle events
    milliStart = pygame.time.get_ticks()
    events = pygame.event.get()
    eventmanager.get().handleEvents(events)

    #Update player and enemies positions/current actions
    currLevel.update()

    #Update camera position using player's
    player_rect = currLevel.get_player_rect()
    camera.updatePosition(player_rect)

    #Fill the screen, draw level, flip the buffer
    screen.fill(constants.DEFAULT_BGCOLOR)
    currLevel.draw(camera)
    pygame.display.flip()

    #Stop timer and sleep for remainder of time
    milliEnd = pygame.time.get_ticks()
    leftover = constants.mSPF - (milliEnd - milliStart)
    if leftover > 0: pygame.time.wait(int(leftover))
