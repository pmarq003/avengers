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
    #TODO need to fix these states --- josh
    def update(self):
        evman = eventmanager.get()
        if evman.LEFTPRESSED:
            self.velX = -self.runVel
            self.orientation = 0
            if(self.velY == 0):
                self.image = pygame.image.load( self.move_left() )
        elif evman.RIGHTPRESSED:
            self.velX = self.runVel
            self.orientation = 1
            if(self.velY == 0):
                self.image = pygame.image.load( self.move_right() )
        else:
            self.velX = 0
            if(self.velY == 0):
                if(self.orientation == 0):
                    self.image = pygame.image.load(self.stand_left)
                else:
                    self.image = pygame.image.load(self.stand_right)

        if evman.SPACEPRESSED and self.canJump:
            self.canJump = False
            self.velY -= self.jumpVel
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
    NUM_MOVEPICS = 4        #number pics in move anim
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #animation images
    jump_left = 'images/america/jump_left.gif'
    jump_right = 'images/america/jump_right.gif'
    stand_left = 'images/america/stand_left.gif'
    stand_right = 'images/america/stand_right.gif'

    #move left animation
    #show each moving animation twice to make it visible
    def move_left(self):
        self.leftMovePic = (self.leftMovePic - 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.leftMovePic / 2)
        return 'images/america/move_left' + str(showpic) + '.gif'

    #move right animation
    #show each moving animation twice to make it visible
    def move_right(self):
        self.rightMovePic = (self.rightMovePic- 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.rightMovePic / 2)
        return 'images/america/move_right' + str(showpic) + '.gif'

class Hulk(Player):
    #movement vars
    runVel = 15     #xcoord movement velocity
    jumpVel = 35    #jumping velocity

    #animation images
    jump_left = 'images/hulk/jump_left.gif'
    jump_right = 'images/hulk/jump_right.gif'
    stand_left = 'images/hulk/stand_left.gif'
    stand_right = 'images/hulk/stand_right.gif'


    #TODO
    def move_left():
        return None

    #TODO
    def move_right():
        return None

class IronMan(Player):
    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #animation images
    jump_left = 'images/ironman/jump_left.gif'
    jump_right = 'images/ironman/jump_right.gif'
    stand_left = 'images/ironman/stand_left.gif'
    stand_right = 'images/ironman/stand_right.gif'

    #TODO
    def move_left():
        return None

    #TODO
    def move_right():
        return None
