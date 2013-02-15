import pygame
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Camera(object):

    def __init__(self,screen):
        self.screen = screen
        self.window = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

    def updatePosition(self,player_rect):
        #camera center on player
        self.window.center = player_rect.center
        #don't let camera go below screen
        if self.window.bottom >= SCREEN_HEIGHT:
            self.window.bottom -= self.window.bottom - SCREEN_HEIGHT
        #don't let camera go out of left-bounds
        if self.window.left < 0:
            self.window.left = 0

    def zeroPosition(self):
        self.window.topleft = (0,0)

    def draw(self,image,position):
        positionOffset = position.move(-self.window.left,-self.window.top)
        self.screen.blit(image,positionOffset)
