import pygame
from animation import StaticAnimation
from pygame.sprite import Sprite

class LevelObject(Sprite):

    base_img_path = None
    can_get_hurt = False
    can_give_hurt = False
    solid = True

    def __init__(self,x,y):
        Sprite.__init__(self)

        #If this isn't set we assume the base class has already loaded its image
        if self.base_img_path:
            self.anim = StaticAnimation( self.base_img_path )

        self.rect = self.anim.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pass

    def draw(self,camera):
        camera.draw(self.anim.get_image(),self.rect)

    def get_rect(self):
        return self.rect

    def try_hurt(self,by):
        if self.can_get_hurt and by.can_give_hurt:
            self.got_hurt(by)

    def die(self):
        pass

#Node class for AI use only
#should give hints to AI on jumping, etc.
class Node(LevelObject):
    base_img_path = 'images/node.jpg'

class BasicPlatform(LevelObject):
    base_img_path = 'images/basicplatform.png'

class BasicPlatform2(LevelObject):
    base_img_path = 'images/basicplatform2.png'

class MarioGround(LevelObject):
    base_img_path = 'images/marioground.png'

class MarioPlatform(LevelObject):
    base_img_path = 'images/marioPlatform.jpg'

class StaticImage(LevelObject):
    def __init__(self,image_path,x,y):
        self.base_img_path = image_path
        LevelObject.__init__(self,x,y)
