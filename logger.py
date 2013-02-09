import pygame
import pygame.sprite
import player
import level
import eventmanager
import levelobject
import camera
import constants

from constants import SCREEN_WIDTH,SCREEN_HEIGHT
from pygame.locals import *

class Logger(object):
	
	def __init__(self, first = None, last = None):
		self.first = first
		self.last = last
		self.replayCanRun = True
	
	def set(self, camera, currLevel, screen):
		self.camera = camera
		self.level = currLevel
		self.screen = screen
	
	def replay(self):
		if self.replayCanRun == True:
			print("replay ran")
			self.replayCanRun = False
			node = self.first
			while node != None:
				eventmanager.get().handleEvents(node.events)
				self.level.update()
				
				#Update camera position using player's
				player_rect = self.level.get_player_rect()
				self.camera.updatePosition(player_rect)
	
				#Fill the screen, draw level, flip the buffer
				self.screen.fill(constants.DEFAULT_BGCOLOR)
				self.level.draw(self.camera)
				pygame.display.flip()
				node = node.next
			self.replayCanRun = True

	def add(self, node):
		if(self.first == None):
			self.first = node
			self.last = node
		else:
			self.last.next = node
			self.last = node
			
#Create singleton accessible through logger.get()
__instance = Logger()
def get(): return __instance
		
class LogNode(object):
	
	def __init__(self, events, next = None):
		self.events = events
		self.next = next