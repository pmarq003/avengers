import pygame

class StaticImage(object):

    def __init__(self,image_path,x,y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pass

    def draw(self,camera):
        camera.draw(self.image,self.rect)
