import player
import eventmanager
import level
import camera
import constants
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

import pygame
from pygame.locals import *

#initialize pygame lib
pygame.init()

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avengers')

#Make a camera (this might need to go inside the level object, but that's ok)
camera = camera.Camera(screen)

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

    #Update camera position using player's
    player_rect = currLevel.get_player_rect()
    camera.updatePosition(player_rect)

    #Stuff that's gonna get cut out
    msg = currLevel.player.message
    msgSurface = fontObj.render(msg, False, (0,0,0))
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (0,0)

    #Fill the screen, draw level, flip the buffer
    screen.fill(constants.DEFAULT_BGCOLOR)
    camera.draw(msgSurface, msgRect)
    camera.draw(logo, logorect)
    currLevel.draw(camera)
    pygame.display.flip()

    #Stop timer and sleep for remainder of time
    milliEnd = pygame.time.get_ticks()
    leftover = constants.mSPF - (milliEnd - milliStart)
    if leftover > 0: pygame.time.wait(int(leftover))
