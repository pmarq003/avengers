import pygame
from pygame.sprite import Sprite

class BasicPlatform(Sprite):
    
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image = pygame.image.load('images/basicplatform.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pass

    def draw(self,camera):
        camera.draw(self.image,self.rect)

    def get_rect(self):
        return self.rect
