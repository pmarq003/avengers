import pygame
from animation import StaticAnimation
from pygame.sprite import Sprite

class LevelObject(Sprite):

    base_img_path = None

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
