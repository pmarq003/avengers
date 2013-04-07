from character import Character
import eventmanager
import sound
import time
from animation import StaticAnimation
from levelobject import TransientEntity
import pygame
import random

class Player(Character):
	can_get_hurt  = True
	can_give_hurt = True
	has_star = False
	attack_timer = 0
	sattack_timer = 0
	sattack_ammo = 10
	timer = time.clock()

	def __init__(self,x,y,level):
		Character.__init__(self,x,y)
		self.facingRight = True
		self.level = level

	def charSpecificUpdate(self):
		
		if (time.clock() - self.timer > 15) and self.has_star :
			self.stopStar()

		evman = eventmanager.get()

		if (evman.SPECPRESSED and self.sattack_ammo > 0) or self.sattack_timer != 0:
			#Special attack takes precedence and stops normal attack
			self.attack_timer = 0

			if self.sattack_timer == 0:
				self.decAmmo()

			self._play_special()
			try: self.special_attack()
			except AttributeError: pass

		elif evman.NORMPRESSED or self.attack_timer != 0: #normal attack pressed

			try: self.special_attack()
			except AttributeError:
	
				if self.isJumping:
					self._load_image( self.jump_attack )
				else:
					self._load_image( self.norm_attack )
	
				#mid attack
				if self.attack_timer > 1:
					self.attacking = True
					self.attack_timer -= 1
					self.velX = self.primary_attack_speed if self.facingRight else -1*self.primary_attack_speed
	
				#start recovery phase
				elif self.attack_timer == 1:
					self.attacking = False
					self.attack_timer = -1*self.primary_attack_recovery
					if not self.isJumping: self.stallX()
	
				#start attack
				elif self.attack_timer == 0:
					self.attacking = True
					self.attack_timer = self.primary_attack_length
					#now plays a random sound which may or may not be captain falcon
					self._play_attack()
	
				#mid recovery
				else:
					self.attacking = False
					self.attack_timer += 1
					if not self.isJumping: self.stallX()


		elif evman.LEFTPRESSED: #left key pressed
			self.velX = -self.runVel
			self.facingRight = False
			self._load_image( self.walk )

		elif evman.RIGHTPRESSED: #right key pressed
			self.velX = self.runVel
			self.facingRight = True
			self._load_image( self.walk )

		else:
			self.velX = 0
			if not self.isJumping:
				self._load_image( self.stand )

		#Attack animation overrides others
		if not self.attacking:
			if self.isJumping:
				self._load_image( self.jump )

			#jumping upwards
			elif evman.SPACEPRESSED:
				self.isJumping = True
				self.velY -= self.jumpVel
				self._load_image( self.jump )
				self._play_jump()

	def got_hurt(self,by):
		if by.can_give_hurt:
			self.die()

	def incAmmo(self):
		self.sattack_ammo = 10 if self.sattack_ammo >= 10 else self.sattack_ammo + 1

	def decAmmo(self):
		self.sattack_ammo = 0 if self.sattack_ammo <= 0 else self.sattack_ammo - 1
	
	def star(self):
		self.can_get_hurt = False
		self.has_star = True
		print("Star power has started.")
		self.timer = time.clock()
		
	def stopStar(self):
		self.can_get_hurt = True
		self.has_star = False
		print("Star power has worn off.")

class CaptainAmerica(Player):
	numWalkFrames = 4		#number pics in move anim
	walkDelay = 2		#delay factor to make anims visible

	#movement vars
	runVel = 10	 #xcoord movement velocity
	jumpVel = 25	#jumping velocity

	animFolder = 'america'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5

class BlackWidow(Player):
	numWalkFrames = 3        #number pics in move anim
	walkDelay = 3        #delay factor to make anims visible

	#movement vars
	runVel = 10     #xcoord movement velocity
	jumpVel = 25    #jumping velocity

	animFolder = 'blackwidow'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5


class Hawkeye(Player):
	numWalkFrames = 4		#number pics in move anim
	walkDelay = 2		#delay factor to make anims visible

	#movement vars
	runVel = 10	 #xcoord movement velocity
	jumpVel = 20	#jumping velocity

	animFolder = 'hawkeye'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5
	
	class ArrowLeft(TransientEntity):
		attacking = True
		can_give_hurt = True
		kill_on_collide = True
		base_img_path = 'images/hawkeye/arrow_left.png'
		timeout = 100

		def update(self):
			TransientEntity.update(self)
			self.rect.left -= 20

	class ArrowRight(TransientEntity):
		attacking = True
		can_give_hurt = True
		kill_on_collide = True
		base_img_path = 'images/hawkeye/arrow_right.png'
		timeout = 100

		def update(self):
			TransientEntity.update(self)
			self.rect.left += 20

	def normal_attack(self):
		self._load_image( self.norm_attack )
		self.stallX()

		#On the second frame the rect for the player will be updated
		#so we can position the lightning correctly relative to that
		if self.sattack_timer == 2:
			if self.facingRight:
				entity = self.ArrowRight(0,0)
				entity.rect.topleft = self.rect.topright
				self.level.addEntity(entity)
			else:
				entity = self.ArrowLeft(0,0)
				entity.rect.topright = self.rect.topleft
				self.level.addEntity(entity)
			self.sattack_timer -= 1

		#mid attack
		elif self.sattack_timer > 1:
			self.sattack_timer -= 1

		#end of attack
		elif self.sattack_timer == 1:
			self.attacking = False
			self.sattack_timer = 0

		#start of attack
		else:
			self.attacking = True
			self.sattack_timer = 5

	def special_attack(self):
		self._load_image( self.norm_attack )
		self.stallX()

		#On the second frame the rect for the player will be updated
		#so we can position the lightning correctly relative to that
		if self.sattack_timer == 2:
			if self.facingRight:
				entity = self.ArrowRight(0,0)
				entity.rect.topleft = self.rect.topright
				self.level.addEntity(entity)
			else:
				entity = self.ArrowLeft(0,0)
				entity.rect.topright = self.rect.topleft
				self.level.addEntity(entity)
			self.sattack_timer -= 1

		#mid attack
		elif self.sattack_timer > 1:
			self.sattack_timer -= 1

		#end of attack
		elif self.sattack_timer == 1:
			self.attacking = False
			self.sattack_timer = 0

		#start of attack
		else:
			self.attacking = True
			self.sattack_timer = 5

class Hulk(Player):
	numWalkFrames = 4		#number pics in move anim
	walkDelay = 2		#delay factor to make anims visible

	#movement vars
	runVel = 25	 #xcoord movement velocity
	jumpVel = 35	#jumping velocity

	animFolder = 'hulk'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5

class IronMan(Player):
	numWalkFrames = 4		#number pics in move anim
	walkDelay = 2		#delay factor to make anims visible

	#movement vars
	runVel = 7	 #xcoord movement velocity
	jumpVel = 25	#jumping velocity

	animFolder = 'ironman'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5

	class BulletLeft(TransientEntity):
		attacking = True
		can_give_hurt = True
		kill_on_collide = True
		base_img_path = 'images/ironman/bullet_left.png'
		timeout = 100

		def update(self):
			TransientEntity.update(self)
			self.rect.left -= 20

	class BulletRight(TransientEntity):
		attacking = True
		can_give_hurt = True
		kill_on_collide = True
		base_img_path = 'images/ironman/bullet_right.png'
		timeout = 100

		def update(self):
			TransientEntity.update(self)
			self.rect.left += 20

	def special_attack(self):
		self._load_image( self.norm_attack )
		self.stallX()

		#On the second frame the rect for the player will be updated
		#so we can position the lightning correctly relative to that
		if self.sattack_timer == 2:
			if self.facingRight:
				entity = self.BulletRight(0,0)
				entity.rect.topleft = self.rect.topright
				self.level.addEntity(entity)
			else:
				entity = self.BulletLeft(0,0)
				entity.rect.topright = self.rect.topleft
				self.level.addEntity(entity)
			self.sattack_timer -= 1

		#mid attack
		elif self.sattack_timer > 1:
			self.sattack_timer -= 1

		#end of attack
		elif self.sattack_timer == 1:
			self.attacking = False
			self.sattack_timer = 0

		#start of attack
		else:
			self.attacking = True
			self.sattack_timer = 5

class Thor(Player):
	numWalkFrames = 5		#number pics in move anim
	walkDelay = 2		#delay factor to make anims visible

	#movement vars
	runVel = 20	 #xcoord movement velocity
	jumpVel = 20	#jumping velocity

	animFolder = 'thor'

	primary_attack_speed = 10
	primary_attack_length = 5
	primary_attack_recovery = 5

	class ThorLightningLeft(TransientEntity):
		attacking = True
		can_give_hurt = True
		base_img_path = 'images/thor/lightning_left.png'
		timeout = 10

	class ThorLightningRight(TransientEntity):
		attacking = True
		can_give_hurt = True
		base_img_path = 'images/thor/lightning_right.png'
		timeout = 10


	def special_attack(self):
		self._load_image( self.jump_attack )
		self.stallX()
		self.velY = -1 #counter gravity

		#On the second frame the rect for the player will be updated
		#so we can position the lightning correctly relative to that
		if self.sattack_timer == 9:
			if self.facingRight:
				entity = self.ThorLightningRight(0,0)
				entity.rect.topleft = self.rect.topright
				self.level.addEntity(entity)
			else:
				entity = self.ThorLightningLeft(0,0)
				entity.rect.topright = self.rect.topleft
				self.level.addEntity(entity)
			self.sattack_timer -= 1

		#mid attack
		elif self.sattack_timer > 1:
			self.sattack_timer -= 1

		#end of attack
		elif self.sattack_timer == 1:
			self.attacking = False
			self.sattack_timer = 0

		#start of attack
		else:
			self.attacking = True
			self.sattack_timer = 10
