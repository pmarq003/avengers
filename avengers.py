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
import hud
import sound
from levelobject import StaticImage
import time

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
		logger.get().setScreen(self.screen)

		#Make a camera (this might need to go inside the level object, but that's ok)
		self.camera = camera.Camera(self.screen)
		logger.get().setCamera(self.camera)

		#number of the current level
		self.levelNumber = 1    #default 1, change for debugging
		self.currLevel = self.getCurrentLevel()
		logger.get().setLevel(self.levelNumber)

		#player starts with 3 lives
		self.player_lives = constants.PLAYER_LIVES

		#menus
		self.startMenu = startmenu.StartMenu()
		self.pauseMenu = pausemenu.PauseMenu()
		logger.get().setMenu(self.startMenu)

		#the hud
		self.hud = hud.HUD()

		#I wanna listen to my music while I develop dammit!
		if "-m" in sys.argv:
			sound.set_bgm_vol(0)
			sound.set_sfx_vol(0)
			self.hud.vol = False

	def update(self):
		#Game loop
		wasplaying = True #Hack to figure out when we need to change sounds
		while True:

			#Start timer and handle events
			milliStart = pygame.time.get_ticks()
			events = pygame.event.get()
			logEvents = eventmanager.get().handleEvents(events)
			#if event = r or pause --> don't log
			if logEvents : logger.get().add(logger.LogNode(events))

			if self.startMenu.isPlaying():

				if not wasplaying: sound.play_bgm(self.currLevel.bgm)

				if not self.currLevel.player_alive:
					self.player_lives -= 1

					logger.get().clear()
					self.loadLevel()

					if self.player_lives < 1:
						self.currLevel.charSelected = False
						self.currLevel.charsel.char = 0
						self.screen.fill(0)
						gameover = StaticImage( "images/gameover.jpg", 0, 0 )
						gameover.rect.topleft = self.camera.window.centerx - gameover.rect.width/2,\
												self.camera.window.centery - gameover.rect.width/2
						gameover.draw(self.camera)
						pygame.display.flip()
						time.sleep(3)
						self.player_lives = constants.PLAYER_LIVES

				self.screen.fill(constants.DEFAULT_BGCOLOR)
				self.currLevel.draw(self.camera)

				if self.currLevel.charSelected:
					self.hud.draw(self.camera, self)
				else:
					self.hud.drawVol(self.camera)

				#Update player and enemies positions/current actions
				if not eventmanager.get().isPaused():
					self.currLevel.update()
					if self.currLevel.charSelected:
						self.hud.update()
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
					#'restart level' clicked 
						self.currLevel = self.getCurrentLevel()
						self.pauseMenu.restartLevel = False
						eventmanager.get().PAUSED = False


				#Update camera position using player's
				player_rect = self.currLevel.get_player_rect()
				self.camera.updatePosition(player_rect)

				#Fill the screen, draw level, flip the buffer
				wasplaying = True
			else:

				#update inputs from startMenu
				if wasplaying: sound.play_bgm(self.startMenu.bgm)
				self.startMenu.update()
				self.camera.zeroPosition()
				self.startMenu.draw(self.camera)
				wasplaying = False

				#'Load Game' clicked
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
		elif self.levelNumber == 2:
			return level.Level2()
		elif self.levelNumber == 3:
			return level.Level3()
		else:
			return None

	def loadLevel(self):
		f = open('save', 'r')
		data = f.readline().split()
		f.close()
		#get level number from save file 
		self.levelNumber = int(data[0])
		#set current level
		self.currLevel = self.getCurrentLevel()
		#set chosen player
		choice = int(data[1])
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
		elif choice == 6:
			self.currLevel.player = player.BlackWidow(0,0,self)
		self.currLevel.charsel.setChar(choice)
		#set player coords
		self.currLevel.player.rect.x = int(data[2])
		self.currLevel.player.rect.y = int(data[3])
		self.currLevel.charSelected = True
		#begin playing level
		self.startMenu.loadLevel = False
		self.startMenu.playing = True


if __name__ == '__main__':
	_game = AvengersGame()
	_game.update()