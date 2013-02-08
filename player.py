import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(Sprite):


    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load(self.stand_right)
        self.orientation = 1 #0 for left, 1 for right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velX = 0
        self.velY = 0
        self.canJump = False

    #updates the players velocities and images
    #orientation is used to track whether the character is facing left or right
    def update(self):
        evman = eventmanager.get()
        if evman.LEFTPRESSED:
            self.velX = -10
            self.orientation = 0
            if(self.velY == 0):
                self.image = pygame.image.load(self.stand_left)
        elif evman.RIGHTPRESSED:
            self.velX = 10
            self.orientation = 1
            if(self.velY == 0):
                self.image = pygame.image.load(self.stand_right)
        else:
            self.velX = 0
            if(self.velY == 0):
                if(self.orientation == 0):
                    self.image = pygame.image.load(self.stand_left)
                else:
                    self.image = pygame.image.load(self.stand_right)

        if evman.SPACEPRESSED and self.canJump:
            self.canJump = False
            self.velY -= 25
            if(self.orientation == 0):
                self.image = pygame.image.load(self.jump_left)
            else:
                self.image = pygame.image.load(self.jump_right)

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
<<<<<<< HEAD
    jump_left = 'images/america/jump_left.gif'
    jump_right = 'images/america/jump_right.gif'
    stand_left = 'images/america/stand_left.gif'
    stand_right = 'images/america/stand_right.gif'
=======
    image_path = 'images/CaptAmericaStanding.png'
>>>>>>> 7cd58fd7fd6a157456207eb66eb49f1149371560
