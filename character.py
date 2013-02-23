import pygame
import eventmanager
import logger
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite

class Character(LevelObject):

	def __init__(self, x, y):
		#general stuff
		self.alive = True
		self.isJumping = False   #used to detect the peak of player's jump
		self.facingRight = True  #player facing right?
		self.attacking = False   #player attacking?


		#During an update it's possible the sprite changed, changing the rect size.
		#In this case we need to update the character's rect object to reflect the new
		#sprite size. However if the charspecificupdate already handled the changing
		#rect size then we don't want to overwrite it afterwards, so in that case this
		#should be set false
		self.fixRectAfterUpdate = True

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

	#updates the players velocities and animations
	#orientation is used to track whether the character is facing left or right
	def update(self):
		self.anim.update()

		#If we're not alive don't process anything
		if self.alive:

			evman = eventmanager.get()

			#replay
			if evman.REPLAYPRESSED and logger.get().replayCanRun:
				logger.get().replay()

			#Do any updates pertaining to the child character class.
			#If the child class hasn't implemented the method, don't worry about it
			try: self.charSpecificUpdate()
			except AttributeError: pass

		if self.fixRectAfterUpdate:
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
