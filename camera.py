import pygame
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Camera(object):

    def __init__(self,screen):
        self.screen = screen
        self.window = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

    def updatePosition(self,player_rect): 
        self.window.center = player_rect.center 

    def draw(self,image,position):
        positionOffset = position.move(-self.window.left,-self.window.top)
        self.screen.blit(image,positionOffset)
