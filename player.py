import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velX = 0
        self.velY = 0
        self.canJump = False

    def update(self):
        evman = eventmanager.get()
        if evman.LEFTPRESSED:    self.velX = -10
        elif evman.RIGHTPRESSED: self.velX = 10
        else:                    self.velX = 0


        if evman.SPACEPRESSED and self.canJump:
            self.canJump = False
            self.velY -= 25

        #Oh snap gravity!
        self.velY += 1
        self.rect.move_ip(self.velX,self.velY)

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
    image_path = 'images/Captain_America_FB_Artwork_3.png'
