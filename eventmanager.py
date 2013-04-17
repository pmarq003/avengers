import sys
import pygame
from types import ListType
from pygame.locals import *

class EventManager:

	def __init__(self):
		self.PAUSED = False
		self.LEFTPRESSED = False
		self.RIGHTPRESSED = False
		self.UPPRESSED = False
		self.DOWNPRESSED = False
		self.SPACEPRESSED = False
		self.NORMPRESSED = False    #normal attack
		self.SPECPRESSED = False    #special attack
		self.REPLAYPRESSED = False  #replay
		self.MOUSE1PRESSED = False
		self.MOUSE1CLICK   = False  #Could be False or the event object
		self.PAUSEPRESSED = False 
		self.keylog = []
		self.cheats = False


	def handleEvents(self,events):
		"""Deal with all the events from pygame. The events have to be passed in since
		pygame wasn't actually initalized in this module"""
		returnVal = True

		#Reset the mouse click, we assume it hasn't been clicked this tick
		self.MOUSE1CLICK = False
		for event in events:
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				print("Exiting....")
				pygame.quit()
				sys.exit(0)

			elif event.type == MOUSEMOTION:     pass
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1: self.MOUSE1PRESSED = True

			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.MOUSE1PRESSED = False
					self.MOUSE1CLICK = event

			elif event.type == KEYDOWN or event.type == KEYUP:
				if   event.key == K_LEFT  : 
					self.LEFTPRESSED  = event.type == KEYDOWN
				elif event.key == K_RIGHT : 
					self.RIGHTPRESSED = event.type == KEYDOWN
				elif event.key == K_UP    : 
					self.UPPRESSED    = event.type == KEYDOWN
				elif event.key == K_DOWN  : 
					self.DOWNPRESSED  = event.type == KEYDOWN
				elif event.key == K_SPACE : self.SPACEPRESSED = event.type == KEYDOWN
				elif event.key == K_SPACE : self.SPACEPRESSED = event.type == KEYDOWN
				elif event.key == K_a     : 
					self.NORMPRESSED = event.type == KEYDOWN
				elif event.key == K_s     : self.SPECPRESSED = event.type == KEYDOWN
				elif event.key == K_r     : 
				    self.REPLAYPRESSED = event.type == KEYDOWN
				    returnVal = False
				elif event.key == K_p and event.type == KEYDOWN: 
					self.PAUSED = not self.PAUSED
					self.PAUSEPRESSED = event.type == KEYDOWN
					returnVal = False
			if event.type == KEYDOWN :
				if   event.key == K_LEFT  : 
					self.keylog.append('l')
				elif event.key == K_RIGHT : 
					self.keylog.append('r')
				elif event.key == K_UP    : 
					self.keylog.append('u')
				elif event.key == K_DOWN  : 
					self.keylog.append('d')
				elif event.key == K_a     : 
					self.keylog.append('a')
				elif event.key == K_b     : 
					self.keylog.append('b')
		self.keylog = self.keylog[-10:]
		if self.keylog == ['u','u','d','d','l','r','l','r','b','a']:
			self.cheats = True
			print("Cheats activated, pussy...")
			self.keylog = []			
		return returnVal			
			

	def isPaused(self):
		return self.PAUSED
	def togglePause(self):
		self.PAUSED = not self.PAUSED


#Create singleton accessible through eventmanager.get()
__instance = EventManager()
def get(): return __instance
