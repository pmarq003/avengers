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

        #number of the current level
        self.levelNumber = 1
        self.currLevel = self.getCurrentLevel()

        #menus
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
                    self.currLevel = self.getCurrentLevel()

                self.screen.fill(constants.DEFAULT_BGCOLOR)
                self.currLevel.draw(self.camera)

                #Update player and enemies positions/current actions
                if not eventmanager.get().isPaused():
                    self.currLevel.update()
                else:
                #show pause menu
                    self.pauseMenu.draw(self.camera)
                    self.pauseMenu.update()
                    #'quit to main' clicked
                    if self.pauseMenu.showMainMenu:
                        self.startMenu.playing = False
                        self.currLevel = self.getCurrentLevel()
                        self.pauseMenu.showMainMenu = False
                        eventmanager.get().PAUSED = False
                    elif self.pauseMenu.restartLevel:
                        self.currLevel = self.getCurrentLevel()
                        self.pauseMenu.restartLevel = False
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

                if self.startMenu.loadLevel == True:
                    self.loadLevel()


            pygame.display.flip()

            #Stop timer and sleep for remainder of time
            milliEnd = pygame.time.get_ticks()
            leftover = constants.mSPF - (milliEnd - milliStart)
            if leftover > 0: pygame.time.wait(int(leftover))

    def getCurrentLevel(self):
        if self.levelNumber == 0:
            return None
        elif self.levelNumber == 1:
            return level.Level1()
        else:
            return None

    def loadLevel(self):
        #get level number from save file (from start menu)
        self.levelNumber = self.startMenu.levelNumber
        #set current level
        self.currLevel = self.getCurrentLevel()
        choice = self.startMenu.charChoice
        #set chosen player
        if choice == 1:
            self.currLevel.player = player.Hulk(0,0,self)
        elif choice == 2:
            self.currLevel.player = player.Thor(0,0,self)
        elif choice == 3:
            self.currLevel.player = player.CaptainAmerica(0,0,self)
        elif choice == 4:
            self.currLevel.player = player.IronMan(0,0,self)
        elif choice == 5:
            self.currLevel.player = player.Hawkeye(0,0,self)
        #set player coords
        self.currLevel.player.rect.x = self.startMenu.currentX
        self.currLevel.player.rect.y = self.startMenu.currentY
        self.currLevel.charSelected = True
        #begin playing level
        self.startMenu.loadLevel = False
        self.startMenu.playing = True



if __name__ == '__main__':
    _game = AvengersGame()
    _game.update()


