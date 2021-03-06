import pygame
import eventmanager
import logger
import sound
import random
import time
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite

class Character(LevelObject):

	def __init__(self, x, y):
		#general stuff
		self.alive = True
		self.isJumping = False   #used to detect the peak of player's jump
		self.facingRight = False #player facing right?
		self.attacking = False   #player attacking?
		self.set_blink = False
		self.has_star = False

		self.velX = 0
		self.velY = 0

		#load images and do rest of constructor
		self.__populate_image_variables()
		self.anim = None
		self._load_image( self.stand )
		LevelObject.__init__(self,x,y)
	

	def _load_image( self, img_tuple ):
		left,right = img_tuple
		toset = None
		if self.facingRight: toset = right
		else:				toset = left

		if not toset == self.anim:
			toset.reset()
		self.anim = toset
		
		if self.has_star and self.anim.blink == False:
			self.anim.blink = True
		elif self.has_star == False:
		    self.anim.blink = False

	def _play_attack(self):
		soundd = self.animFolder
		sound.play_sfx('sounds/sfx/' + soundd + '/hit (%s).wav' % random.randint(1, 7))

	def _play_jump(self):
		soundd = self.animFolder
		sound.play_sfx('sounds/sfx/' + soundd + '/jump.wav')

	def _play_special(self):
		soundd = self.animFolder
		sound.play_sfx('sounds/sfx/' + soundd + '/special.wav')

	#updates the players velocities and animations
	#orientation is used to track whether the character is facing left or right
	def update(self):
		self.anim.update()
		#If we're not alive don't process anything
		if self.alive:
			#Do any updates pertaining to the child character class.
			#If the child class hasn't implemented the method, don't worry about it
			try: self.charSpecificUpdate()
			except AttributeError: pass
			evman = eventmanager.get()
			
			#replay
			#if evman.REPLAYPRESSED and logger.get().replayCanRun:
			#	logger.get().replay()
			#	logger.get().replayCanRun = True

		#update rect with new image
		#we use bottomleft so it doesn't mess with collision detection
		oldxy = self.rect.bottomleft
		self.rect = self.anim.get_rect()
		self.rect.bottomleft = oldxy

		#Oh snap gravity!
		self.velY += 1
		self.rect.move_ip(self.velX,self.velY)

	def die(self):
		self.velY = -15
		self.stallX()
		self.alive = False
		self.solid = False
		self._load_image( self.jump )
		self.anim.blink = True
		
	def blink(self, boolean):  
		#self._load_image( self.stand )
		self.anim.blink = boolean
		if boolean: print("blink set to true")
		else: print("blink set to false")

	def stallX(self):
		self.velX = 0

	def stallY(self):
		self.velY = 0

	def stall(self):
		self.stallX()
		self.stallY()

	def __populate_image_variables(self):
		animd = self.animFolder
		self.norm_attack = StaticAnimation('images/' + animd + '/norm_attack_left.gif'),\
						   StaticAnimation('images/' + animd + '/norm_attack_right.gif')
		self.jump_attack = StaticAnimation('images/' + animd + '/jump_attack_left.gif'),\
						   StaticAnimation('images/' + animd + '/jump_attack_right.gif')
		#self.spec_attack = StaticAnimation(''),\
		#				   StaticAnimation('')
		self.jump		=  StaticAnimation('images/' + animd + '/jump_left.gif'),\
						   StaticAnimation('images/' + animd + '/jump_right.gif')
		self.stand	   =   StaticAnimation('images/' + animd + '/stand_left.gif'),\
						   StaticAnimation('images/' + animd + '/stand_right.gif')
		self.walk		=  Animation('images/' + animd + '/move_left{0}.gif',  self.numWalkFrames, self.walkDelay ),\
						   Animation('images/' + animd + '/move_right{0}.gif', self.numWalkFrames, self.walkDelay )
