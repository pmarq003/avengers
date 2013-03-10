import pygame
import pygame.sprite
import player
import level
import eventmanager
import levelobject
import camera
import constants
import startmenu
import time

from constants import SCREEN_WIDTH,SCREEN_HEIGHT
from pygame.locals import *
from threading import Lock

class Logger(object):
	
	def __init__(self, first = None, last = None):
		self.first = first
		self.last = last
		self.char = 0
		self.currLevel = None
		self.lock = Lock()
		self.timer = time.clock()
		self.levelNumber = 0
		self.x = 0
		self.y = 500
		
	def setCamera(self, camera):
		self.camera = camera
		
	def getLevel(self, levelNumber):
		if self.levelNumber == 0:
			self.currLevel = level.Level0(self.avengersObj)
		elif self.levelNumber == 1:
			self.currLevel = level.Level1(self.avengersObj)
		elif self.levelNumber == 2:
			self.currLevel = level.Level2(self.avengersObj)
		elif self.levelNumber == 3:
			self.currLevel = level.Level3(self.avengersObj)
		elif self.levelNumber == 4:
			self.currLevel = level.Level4(self.avengersObj)
		elif self.levelNumber == 5:
			self.currLevel = level.Level5(self.avengersObj)
		else:
			self.currLevel = None
					
	def setAvengersObj(self, avengersObj):
		self.avengersObj = avengersObj
			
	def setLevel(self, levelNumber):
		self.levelNumber = levelNumber
	
	def setScreen(self, screen):
		self.screen = screen
	
	def setMenu(self, startMenu):
		self.startMenu = startMenu
	
	def setChar(self, char):
		self.char = char
	
	def setStart(self, x,y): 
		self.x = x
		self.y = y
		
	def loadChar(self):
		f = open('replay', 'r')
		data = f.readline().split()
		f.close()
		self.levelNumber = int(data[0])
		self.char = int(data[1])
	
	def replay(self):
		if time.clock() - self.timer > 2 :
			node = self.first
			self.loadChar()			    
			self.getLevel(self.levelNumber)
			self.currLevel.setPlayer(self.char, 0, 0)
			self.currLevel.player.rect.x = int(self.x)
			self.currLevel.player.rect.y = int(self.y)
			self.currLevel.player.can_get_hurt = False
			self.currLevel.plotOver = True
			while node != None:
				milliStart = pygame.time.get_ticks()
				eventmanager.get().handleEvents(node.events)
				if self.currLevel.levelNumber == 0:
					self.screen.fill(constants.LEVEL0_BGCOLOR)
				elif self.currLevel.levelNumber == 1:
					self.screen.fill(constants.LEVEL1_BGCOLOR)
				else:
					self.screen.fill(constants.DEFAULT_BGCOLOR)
				self.currLevel.draw(self.camera)
				self.currLevel.update()
				player_rect = self.currLevel.get_player_rect()
				self.camera.updatePosition(player_rect)
				pygame.display.flip()

				#Stop timer and sleep for remainder of time
				milliEnd = pygame.time.get_ticks()
				leftover = constants.mSPF - (milliEnd - milliStart)
				if leftover > 0: pygame.time.wait(int(leftover))
				node = node.next
			print("replay ran")
			self.timer = time.clock()
		else:
			print("false replay stopped")

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