import camera
import constants
import eventmanager
import level
import player
import pygame
import time
import logger
import startmenu
import sound

from pygame.locals import *
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

import os
import sys

isPaused = False

#center screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

#initialize pygame lib
pygame.init()

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Avengers - Six Guys')

#Make a camera (this might need to go inside the level object, but that's ok)
camera = camera.Camera(screen)

currLevel = level.Level1()

startMenu = startmenu.StartMenu()

logger.get().set(camera, currLevel, screen, startMenu)

#I wanna listen to my music while I develop dammit!
if "-m" in sys.argv:
    startMenu.vol = False

#Game loop
wasplaying = True #Hack to figure out when we need to change sounds
while True:

    #Start timer and handle events
    milliStart = pygame.time.get_ticks()
    events = pygame.event.get()
    isPaused = eventmanager.get().handleEvents(events)
    logger.get().add(logger.LogNode(events))

    if startMenu.isPlaying():

        if not wasplaying: sound.play_bgm(currLevel.bgm)

        if not currLevel.player_alive:
            logger.get().clear()
            currLevel = level.Level1()

        screen.fill(constants.DEFAULT_BGCOLOR)
        currLevel.draw(camera)

        #Update player and enemies positions/current actions
        if not isPaused:
            currLevel.update()

        #Update camera position using player's
        player_rect = currLevel.get_player_rect()
        camera.updatePosition(player_rect)

        #Fill the screen, draw level, flip the buffer
        wasplaying = True
    else:

        if wasplaying: sound.play_bgm(startMenu.bgm)
        startMenu.update()
        camera.zeroPosition()
        startMenu.draw(camera)
        wasplaying = False

    pygame.display.flip()

    #Stop timer and sleep for remainder of time
    milliEnd = pygame.time.get_ticks()
    leftover = constants.mSPF - (milliEnd - milliStart)
    if leftover > 0: pygame.time.wait(int(leftover))


