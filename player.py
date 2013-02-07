import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(Sprite):

    def __init__(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velX = 0
        self.velY = 0
        self.canJump = False

    def update(self):
        evman = eventmanager.get()
        if evman.LEFTPRESSED:
            self.rect = self.rect.move(-10,0)

        if evman.RIGHTPRESSED:
            self.rect = self.rect.move(10,0)

        if evman.SPACEPRESSED and self.canJump:
            self.canJump = False
            self.velY -= 25 

        #Oh snap gravity!
        self.velY += 1
        self.rect = self.rect.move(self.velX,self.velY)

    def draw(self,camera):
        camera.draw(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def stallX(self):
        self.velX = 0

    def stallY(self):
        self.velY = 0

    def stall(self):
        self.stallX()
        self.stallY()

class CaptainAmerica(Player):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
