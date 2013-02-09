import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(Sprite):

    isJumping = False   #used to detect the peak of player's jump
    peaking = False     #is player at the peak of its jump?
    facingRight = True

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load(self.stand_right)
        self.facingRight = True
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
            self.velX = -self.runVel
            self.facingRight = False
            if(self.velY == 0):
                self.image = pygame.image.load( self.move_left() )
        elif evman.RIGHTPRESSED:
            self.velX = self.runVel
            self.facingRight = True
            if(self.velY == 0):
                self.image = pygame.image.load( self.move_right() )
        else:
            self.velX = 0
            if(self.velY == 0):
                if(not self.facingRight):
                    self.image = pygame.image.load(self.stand_left)
                else:
                    self.image = pygame.image.load(self.stand_right)

        #jumping upwards
        if evman.SPACEPRESSED and self.canJump:
            self.isJumping = True
            self.canJump = False
            self.velY -= self.jumpVel
            if(not self.facingRight):
                self.image = pygame.image.load(self.jump_left)
            else:
                self.image = pygame.image.load(self.jump_right)

        #downward falling animation
        if(self.velY > 0):
            self.isJumping = False
            if(not self.facingRight):
                self.image = pygame.image.load(self.fall_left)
            else:
                self.image = pygame.image.load(self.fall_right)

        #detect frame after peak jump 
        #show peak frame for consistency
        if(self.peaking):
            self.peaking = False
            if(not self.facingRight):
                self.image = pygame.image.load(self.jump_peak_left)
            else:
                self.image = pygame.image.load(self.jump_peak_right)

        #detect jump peak
        if(self.velY == 0 and self.isJumping):
            self.peaking = True
            if(not self.facingRight):
                self.image = pygame.image.load(self.jump_peak_left)
            else:
                self.image = pygame.image.load(self.jump_peak_right)


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
    DELAY_FACTOR = 2        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #animation images
    fall_left = 'images/america/jump_left.gif'
    fall_right = 'images/america/jump_right.gif'
    jump_left = 'images/america/jump_left.gif'
    jump_right = 'images/america/jump_right.gif'
    jump_peak_left = 'images/america/jump_left.gif'
    jump_peak_right = 'images/america/jump_right.gif'
    stand_left = 'images/america/stand_left.gif'
    stand_right = 'images/america/stand_right.gif'

    #move left animation
    #delay anim to make it visible
    def move_left(self):
        self.leftMovePic = (self.leftMovePic - 1) % (self.DELAY_FACTOR*self.NUM_MOVEPICS)
        showpic = (int) (self.leftMovePic / self.DELAY_FACTOR)
        return 'images/america/move_left' + str(showpic) + '.gif'

    #move right animation
    #delay anim to make it visible
    def move_right(self):
        self.rightMovePic = (self.rightMovePic- 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.rightMovePic / 2)
        return 'images/america/move_right' + str(showpic) + '.gif'

class Hulk(Player):
    NUM_MOVEPICS = 4        #number pics in move anim
    DELAY_FACTOR = 2        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 25     #xcoord movement velocity
    jumpVel = 35    #jumping velocity

    #animation images
    fall_left = 'images/hulk/jump_left.gif'
    fall_right = 'images/hulk/jump_right.gif'
    jump_left = 'images/hulk/jump_left.gif'
    jump_right = 'images/hulk/jump_right.gif'
    jump_peak_left = 'images/hulk/jump_left.gif'
    jump_peak_right = 'images/hulk/jump_right.gif'
    stand_left = 'images/hulk/stand_left.gif'
    stand_right = 'images/hulk/stand_right.gif'

    #move left animation
    #delay anim to make it visible
    def move_left(self):
        self.leftMovePic = (self.leftMovePic - 1) % (self.DELAY_FACTOR*self.NUM_MOVEPICS)
        showpic = (int) (self.leftMovePic / self.DELAY_FACTOR)
        return 'images/hulk/move_left' + str(showpic) + '.gif'

    #move right animation
    #delay anim to make it visible
    def move_right(self):
        self.rightMovePic = (self.rightMovePic- 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.rightMovePic / 2)
        return 'images/hulk/move_right' + str(showpic) + '.gif'


class IronMan(Player):
    NUM_MOVEPICS = 4        #number pics in move anim
    DELAY_FACTOR = 5        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #animation images
    fall_left = ''
    fall_right = 'images/ironman/jump_peak_right.gif'
    jump_left = 'images/ironman/jump_left.gif'
    jump_right = 'images/ironman/jump_right.gif'
    jump_peak_left = ''
    jump_peak_right = 'images/ironman/jump_peak_right.gif'
    stand_left = 'images/ironman/stand_left.gif'
    stand_right = 'images/ironman/stand_right.gif'

    #move left animation
    #delay anim to make it visible
    def move_left(self):
        self.leftMovePic = (self.leftMovePic - 1) % (self.DELAY_FACTOR*self.NUM_MOVEPICS)
        showpic = (int) (self.leftMovePic / self.DELAY_FACTOR)
        return 'images/ironman/move_left' + str(showpic) + '.gif'

    #move right animation
    #delay anim to make it visible
    def move_right(self):
        self.rightMovePic = (self.rightMovePic- 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.rightMovePic / 2)
        return 'images/ironman/move_right' + str(showpic) + '.gif'
