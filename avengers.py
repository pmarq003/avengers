import camera
import constants
import eventmanager
import level
import player
import pausemenu
import pygame
import time
import logger
import startmenu
import sound

from pygame.locals import *
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

import os
import sys

class AvengersGame:

    def __init__(self):
#center screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'

#initialize pygame lib
        pygame.init()

#creates window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Avengers - Six Guys')

#Make a camera (this might need to go inside the level object, but that's ok)
        self.camera = camera.Camera(self.screen)

        self.currLevel = level.Level1()

        self.startMenu = startmenu.StartMenu()
        self.pauseMenu = pausemenu.PauseMenu()

        logger.get().set(self.camera, self.currLevel, self.screen, self.startMenu)

#I wanna listen to my music while I develop dammit!
        if "-m" in sys.argv:
            startMenu.vol = False

    def update(self):
#Game loop
        wasplaying = True #Hack to figure out when we need to change sounds
        while True:

            #Start timer and handle events
            milliStart = pygame.time.get_ticks()
            events = pygame.event.get()
            eventmanager.get().handleEvents(events)
            logger.get().add(logger.LogNode(events))

            if self.startMenu.isPlaying():

                if not wasplaying: sound.play_bgm(self.currLevel.bgm)

                if not self.currLevel.player_alive:
                    logger.get().clear()
                    self.currLevel = level.Level1()

                self.screen.fill(constants.DEFAULT_BGCOLOR)
                self.currLevel.draw(self.camera)

                #Update player and enemies positions/current actions
                if not eventmanager.get().isPaused():
                    self.currLevel.update()
                else:
                    self.pauseMenu.draw(self.camera)
                    self.pauseMenu.update()
                    if self.pauseMenu.showMainMenu:
                        self.startMenu.playing = False
                        self.currLevel = level.Level1()
                        self.pauseMenu.showMainMenu = False
                        eventmanager.get().PAUSED = False

                #Update camera position using player's
                player_rect = self.currLevel.get_player_rect()
                self.camera.updatePosition(player_rect)

                #Fill the screen, draw level, flip the buffer
                wasplaying = True
            else:

                if wasplaying: sound.play_bgm(self.startMenu.bgm)
                self.startMenu.update()
                self.camera.zeroPosition()
                self.startMenu.draw(self.camera)
                wasplaying = False

            pygame.display.flip()

            #Stop timer and sleep for remainder of time
            milliEnd = pygame.time.get_ticks()
            leftover = constants.mSPF - (milliEnd - milliStart)
            if leftover > 0: pygame.time.wait(int(leftover))


if __name__ == '__main__':
    _game = AvengersGame()
    _game.update()


