import pygame
import pygame.sprite
import player
import level
import eventmanager
import levelobject
import camera
import constants
import startmenu

from constants import SCREEN_WIDTH,SCREEN_HEIGHT
from pygame.locals import *

class Logger(object):
	
	def __init__(self, first = None, last = None):
		self.first = first
		self.last = last
		self.replayCanRun = True
		self.char = 0
	
	def set(self, camera, currLevel, screen, startMenu):
		self.camera = camera
		self.currLevel = currLevel
		self.screen = screen
		self.startMenu = startMenu
	
	def setPlayer(self, char):
		self.char = char
	
	def replay(self):
		if self.replayCanRun == True:
			self.replayCanRun = False
			#start from the beginning of the level
			self.currLevel = level.Level1()
			
			if self.char == 1:
				self.currLevel.player = player.Hulk(0,0,self.currLevel)
			elif self.char == 2:
				self.currLevel.player = player.Thor(0,0,self.currLevel)
			elif self.char == 3:
				self.currLevel.player = player.CaptainAmerica(0,0,self.currLevel)
			elif self.char == 4:
				self.currLevel.player = player.IronMan(0,0,self.currLevel)
			elif self.char == 5:
				self.currLevel.player = player.Hawkeye(0,0,self.currLevel)
			
			self.currLevel.charSelected = True
			self.startMenu.update()
			self.camera.zeroPosition()
			self.startMenu.draw(self.camera)
			print("replay ran")
			node = self.first
			while node != None:
				milliStart = pygame.time.get_ticks()
				eventmanager.get().handleEvents(node.events)

				if self.startMenu.isPlaying():

					if not self.currLevel.player_alive:
						self.currLevel = level.Level1()

					#Update player and enemies positions/current actions
					self.currLevel.update()

					#Update camera position using player's
					player_rect = self.currLevel.get_player_rect()
					self.camera.updatePosition(player_rect)

					#Fill the screen, draw level, flip the buffer
					self.screen.fill(constants.DEFAULT_BGCOLOR)
					self.currLevel.draw(self.camera)

				else:

					self.startMenu.update()
					self.camera.zeroPosition()
					self.startMenu.draw(self.camera)

				pygame.display.flip()

				#Stop timer and sleep for remainder of time
				milliEnd = pygame.time.get_ticks()
				leftover = constants.mSPF - (milliEnd - milliStart)
				if leftover > 0: pygame.time.wait(int(leftover))			    
				
				node = node.next
			
			self.replayCanRun = True

	def add(self, node):
		if(self.first == None):
			self.first = node
			self.last = node
		else:
			self.last.next = node
			self.last = node
			
	def clear(self): #python automatically handles garbage collection supposedly - can't find a way to delete objects
		self.first = None
		self.last = None
			
#Create singleton accessible through logger.get()
__instance = Logger()
def get(): return __instance
		
class LogNode(object):
	
	def __init__(self, events, next = None):
		self.events = events
		self.next = next
		self.player = player