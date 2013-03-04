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

    def update(self):
        pass

    def _handleNodeCollision(self):
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

    def die(self):
        pass

#Node class for AI and terrain use only
#should give hints to AI on jumping, etc.
#tells terrain where to move
class Node(LevelObject):
    base_img_path = 'images/node.jpg'


#   Basic level objects...

class BasicPlatform(LevelObject):
    base_img_path = 'images/basicplatform.png'

class BasicPlatform2(LevelObject):
    base_img_path = 'images/basicplatform2.png'

#    Mario-related level objects

class MarioGround1632(LevelObject):
    base_img_path = 'images/levelsprites/smw/marioground1632.png'

class MarioGroundLeft(LevelObject):
    base_img_path = 'images/levelsprites/smw/marioground_left.png'

class MarioGroundRight(LevelObject):
    base_img_path = 'images/levelsprites/smw/marioground_right.png'

class MarioPlatform6(LevelObject):
    base_img_path = 'images/levelsprites/smw/marioplatform6.png'

class MarioMushroomPlatform(LevelObject):
    base_img_path = 'images/levelsprites/smw/mariomushplat.png'

class MarioMovablePlatform(LevelObject):
    base_img_path = 'images/levelsprites/smw/marioground.png'

    def update(self):
		self.rect.move_ip(self.velX,self.velY)

    def handleNodeCollision(self, node):
        self.velX *= node.xmult
        self.velY *= node.ymult

class MarioCloud(LevelObject):
    base_img_path = 'images/levelsprites/smw/mariocloud.png'

#    Sonic-related level objects

class SonicPlatformThick4(LevelObject):
    base_img_path = 'images/levelsprites/sonic/sonicplatform_thick4.jpg'

class SonicPlatformThick(LevelObject):
    base_img_path = 'images/levelsprites/sonic/sonicplatform_thick.jpg'
    
class SonicPlatform(LevelObject):
    base_img_path = 'images/levelsprites/sonic/sonicplatform.jpg'

#   Other stuff 

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
