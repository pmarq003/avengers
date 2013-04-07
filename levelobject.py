import pygame
from animation import StaticAnimation
from pygame.sprite import Sprite

class LevelObject(Sprite):

	base_img_path = None
	can_get_hurt = False
	can_give_hurt = False
	solid = True

	def __init__(self,x,y,velX=0,velY=0,xmult=0,ymult=0):
		Sprite.__init__(self)
		#optional terrain velocities
		self.velX = velX
		self.velY = velY
		#optional terrain velocity multipliers
		self.xmult = xmult
		self.ymult = ymult
		#If this isn't set we assume the base class has already loaded its image
		if self.base_img_path:
			self.anim = StaticAnimation( self.base_img_path )

		self.rect = self.anim.get_rect()
		self.rect.topleft = (x,y)

	#implement in specific classes
	def update(self):
		pass

	#implement in specific classes
	def handleNodeCollision(self, node):
		pass

	def draw(self,camera):
		image = self.anim.get_image()
		if image != None:
			camera.draw(image,self.rect)

	def get_rect(self):
		return self.rect

	def try_hurt(self,by):
		if self.can_get_hurt and by.can_give_hurt:
			self.got_hurt(by)
		elif by.can_get_hurt and self.can_give_hurt:
			by.got_hurt(self)

	def die(self):
		pass

#Node class for AI and terrain use only
#should give hints to AI on jumping, etc.
#tells terrain where to move
class Node(LevelObject):
	base_img_path = 'images/node.jpg'

class Node500(LevelObject):
	base_img_path = 'images/node500.jpg'

#   Tutorial level objects


class TutGround(LevelObject):
	base_img_path = 'images/levelsprites/tut/tutground.gif'

class TutSign1(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign1.gif'

class TutSign2(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign2.gif'

class TutSign3(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign3.gif'

class TutSign4(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign4.gif'

class TutSign5(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign5.gif'

class TutSign6(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/tut/tutsign6.gif'


#    Mario-related level objects


class MarioGround1632(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioground1632.png'

class MarioGroundLeft(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioground_left.png'

class MarioGroundRight(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioground_right.png'

class MarioPlatform6(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioplatform6.gif'

class MarioPlatform12(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioplatform12.png'

class MarioMushroomPlatform(LevelObject):
	base_img_path = 'images/levelsprites/smw/mariomushplat.png'

class MarioMushroomPlatformBase(LevelObject):
	base_img_path = 'images/levelsprites/smw/marioplatformtubing.png'

class MarioMovablePlatform(LevelObject):
	base_img_path = 'images/levelsprites/smw/mariomovableplat.png'

	def update(self):
		self.rect.move_ip(self.velX,self.velY)

	def handleNodeCollision(self, node):
		self.velX *= node.xmult
		self.velY *= node.ymult
		
class MarioCastle(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/smw/castle.gif'

class MarioCloud(LevelObject):
	base_img_path = 'images/levelsprites/smw/mariocloud.png'


#    Sonic-related level objects


class SonicPlatformThick4(LevelObject):
	base_img_path = 'images/levelsprites/sonic/sonicplatform_thick4.jpg'

class SonicPlatformThick(LevelObject):
	base_img_path = 'images/levelsprites/sonic/sonicplatform_thick.jpg'
	
class SonicPlatform(LevelObject):
	base_img_path = 'images/levelsprites/sonic/sonicplatform.jpg'
	
class SonicPlatformThin(LevelObject):
	base_img_path = 'images/levelsprites/sonic/sonicplatform_thin.gif'

class MetroidGround(LevelObject):
	base_img_path = 'images/levelsprites/metroid/ground.png'

class MetroidPlatform(LevelObject):
	base_img_path = 'images/levelsprites/metroid/platform.png'

class MetroidMovablePlatform(MarioMovablePlatform):
	base_img_path = 'images/levelsprites/metroid/platform.png'


#    MegaMan-related level objects


class MegamanPlatNorm(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatNorm.gif'

class MegamanPlatThin(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatThin.gif'

class MegamanPlatThin2(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatThin2.gif'
	
class MegamanPlatThin3(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatThin3.gif'

class MegamanPlatLong(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatLong.gif'
	
class MegamanPlatTall(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatTall.gif'
	
class MegamanPlatTaller(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatTaller.gif'
	
class MegamanPlatTallerWide(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatTallerWide.gif'
	
class MegamanPlatTallestWide(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatTallestWide.gif'
	
class MegamanPlatTallest(LevelObject):
	base_img_path = 'images/levelsprites/megaman/PlatTallest.gif'
	
class MegamanMovablePlat(MarioMovablePlatform):
	base_img_path = 'images/levelsprites/megaman/PlatThin.gif'
	
class MegamanMovablePlat2(MarioMovablePlatform):
	base_img_path = 'images/levelsprites/megaman/PlatThin2.gif'
	
class MegamanMovablePlat3(MarioMovablePlatform):
	base_img_path = 'images/levelsprites/megaman/PlatThin3.gif'
	
class Serenity(LevelObject):
	base_img_path = 'images/levelsprites/megaman/serenity.png'


#   Other stuff 


class Checkpoint(LevelObject):
	solid = False
	base_img_path = 'images/levelsprites/checkpoint.gif'

class StaticImage(LevelObject):
	def __init__(self,image_path,x,y):
		self.base_img_path = image_path
		LevelObject.__init__(self,x,y)

class TransientEntity(LevelObject):
	attacking = False
	kill_on_collide = False

	def update(self):
		self.timeout -= 1
		if self.timeout < 0: self.kill()

class Heart(LevelObject):
	solid = False
	base_img_path = 'images/heart.png'

class Ammo(LevelObject):
	solid = False
	base_img_path = 'images/ammo.png'
	
class Star(LevelObject):
	solid = False
	base_img_path = 'images/star.png'
