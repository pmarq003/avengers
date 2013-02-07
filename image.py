import pygame
from pygame.sprite import Sprite

class StaticImage(Sprite):

    def __init__(self,image_path,x,y):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pass

    def draw(self,camera):
        camera.draw(self.image,self.rect)
