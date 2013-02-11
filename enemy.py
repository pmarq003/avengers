import pygame
import eventmanager
import logger
import levelobject
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite

class Enemy(LevelObject):

	def __init__(self, x, y):
		#general stuff
		self.isJumping = False   #used to detect the peak of player's jump
		self.peaking = False     #is player at the peak of its jump?
		self.facingRight = True  #player facing right?
		self.attacking = False   #player attacking?
		self.canJump = False
		self.velX = 0
		self.velY = 0

		#load images and do rest of constructor
		self.__populate_image_variables()
		self.anim = None
		self.__load_image( self.stand )
		LevelObject.__init__(self,x,y)


	def __load_image( self, img_tuple ):
		left,right = img_tuple
		toset = None
		if self.facingRight: toset = right
		else:                toset = left

		if not toset == self.anim:
			toset.reset()
		self.anim = toset

	#updates the players velocities and animations
	#orientation is used to track whether the character is facing left or right
	def update(self):
		self.anim.update()
		evman = eventmanager.get()
#		if evman.NORMPRESSED:                   #normal attack pressed
#			self.attack = True
#			if(self.velY != 0):
#				self.__load_image( self.jump_attack )
#			else:
#				self.stallX()
#				self.__load_image( self.norm_attack )
#		elif evman.LEFTPRESSED:                 #left key pressed
#			self.velX = -self.runVel
#			self.facingRight = False
#			if(self.velY == 0):
#				self.__load_image( self.walk )
#		elif evman.RIGHTPRESSED:                #right key pressed
#			self.velX = self.runVel
#			self.facingRight = True
#			if(self.velY == 0):
#				self.__load_image( self.walk )
#		else:
#			self.velX = 0
#			if(self.velY == 0):
#				self.__load_image( self.stand )
		#debug
		if(self.velY == 0):
			self.__load_image( self.stand )
				
		#replay
		if evman.REPLAYPRESSED and logger.get().replayCanRun:
			logger.get().replay()

		#jumping upwards
		if evman.SPACEPRESSED and self.canJump:
			self.isJumping = True
			self.canJump = False
			self.velY -= self.jumpVel
			self.__load_image( self.jump )

		#downward falling animation
		if(self.velY > 0):
			self.isJumping = False
			self.canJump = False    #remove if you want to jump in midair while falling
			self.__load_image( self.fall )

		#detect frame after peak jump 
		#show peak frame for consistency
		if(self.peaking):
			self.peaking = False
			self.__load_image( self.jump_peak )

		#detect jump peak
		if(self.velY == 0 and self.isJumping):
			self.peaking = True
			self.__load_image( self.jump_peak )

		#Oh snap gravity!
		self.velY += 1
		self.attacking = False #TODO remove?
		self.rect.move_ip(self.velX,self.velY)

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
		#                   StaticAnimation('')
		self.fall        = StaticAnimation('images/' + animd + '/jump_left.gif'),\
						   StaticAnimation('images/' + animd + '/jump_right.gif')
		self.jump        = StaticAnimation('images/' + animd + '/jump_left.gif'),\
						   StaticAnimation('images/' + animd + '/jump_right.gif')
		self.jump_peak   = StaticAnimation('images/' + animd + '/jump_left.gif'),\
						   StaticAnimation('images/' + animd + '/jump_right.gif')
		self.stand       = StaticAnimation('images/' + animd + '/stand_left.gif'),\
						   StaticAnimation('images/' + animd + '/stand_right.gif')
		self.walk        = Animation('images/' + animd + '/move_left{0}.gif',  self.numWalkFrames, self.walkDelay ),\
						   Animation('images/' + animd + '/move_right{0}.gif', self.numWalkFrames, self.walkDelay )

class CaptainRussia(Enemy):
	numWalkFrames = 4        #number pics in move anim
	walkDelay = 2        #delay factor to make anims visible

	#movement vars
	runVel = 10     #xcoord movement velocity
	jumpVel = 25    #jumping velocity

	animFolder = 'captnRussia'
