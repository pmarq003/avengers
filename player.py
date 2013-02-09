import pygame
import eventmanager
from levelobject import LevelObject
from pygame.sprite import Sprite

class Player(LevelObject):

    def __init__(self, x, y):
        #general stuff
        self.isJumping = False   #used to detect the peak of player's jump
        self.peaking = False     #is player at the peak of its jump?
        self.facingRight = True  #player facing right?
        self.attacking = False   #player attacking?
        self.canJump = False
        self.velX = 0
        self.velY = 0

        #load images and do rest of constructor
        self.__populate_image_variables()
        self.image = self.__load_image( self.stand )
        LevelObject.__init__(self,x,y)


    def __load_image( self, img_tuple ):
        left,right = img_tuple
        if self.facingRight: return pygame.image.load( right )
        else:                return pygame.image.load( left )

    #updates the players velocities and animations
    #orientation is used to track whether the character is facing left or right
    def update(self):
        evman = eventmanager.get()
        if evman.NORMPRESSED:                   #normal attack pressed
            self.attack = True
            if(self.velY != 0):
                self.image = self.__load_image( self.jump_attack )
            else:
                self.stallX()
                self.image = self.__load_image( self.norm_attack )
        elif evman.LEFTPRESSED:                 #left key pressed
            self.velX = -self.runVel
            self.facingRight = False
            if(self.velY == 0):
                self.image = self.__move_left()
        elif evman.RIGHTPRESSED:                #right key pressed
            self.velX = self.runVel
            self.facingRight = True
            if(self.velY == 0):
                self.image = self.__move_right()
        else:
            self.velX = 0
            if(self.velY == 0):
                self.image = self.__load_image( self.stand )

        #jumping upwards
        if evman.SPACEPRESSED and self.canJump:
            self.isJumping = True
            self.canJump = False
            self.velY -= self.jumpVel
            self.image = self.__load_image( self.jump )

        #downward falling animation
        if(self.velY > 0):
            self.isJumping = False
            self.canJump = False    #remove if you want to jump in midair while falling
            self.image = self.__load_image( self.fall )

        #detect frame after peak jump 
        #show peak frame for consistency
        if(self.peaking):
            self.peaking = False
            self.image = self.__load_image( self.jump_peak )

        #detect jump peak
        if(self.velY == 0 and self.isJumping):
            self.peaking = True
            self.image = self.__load_image( self.jump_peak )

        #Oh snap gravity!
        self.velY += 1
        self.attacking = False #TODO remove?
        self.rect.move_ip(self.velX,self.velY)

    def stallX(self):
        self.velX = 0

    def stallY(self):
        self.velY = 0

    def stall(self):
        self.stallX()
        self.stallY()

    def __populate_image_variables(self):
        animd = self.animFolder
        self.norm_attack = 'images/' + animd + '/norm_attack_left.gif', 'images/' + animd + '/norm_attack_right.gif'
        self.jump_attack = 'images/' + animd + '/jump_attack_left.gif', 'images/' + animd + '/jump_attack_right.gif'
        self.spec_attack = ''                                         , ''
        self.fall        = 'images/' + animd + '/jump_left.gif'       , 'images/' + animd + '/jump_right.gif'
        self.jump        = 'images/' + animd + '/jump_left.gif'       , 'images/' + animd + '/jump_right.gif'
        self.jump_peak   = 'images/' + animd + '/jump_left.gif'       , 'images/' + animd + '/jump_right.gif'
        self.stand       = 'images/' + animd + '/stand_left.gif'      , 'images/' + animd + '/stand_right.gif'

    #move left animation
    #delay anim to make it visible
    def __move_left(self):
        self.leftMovePic = (self.leftMovePic - 1) % (self.DELAY_FACTOR*self.NUM_MOVEPICS)
        showpic = (int) (self.leftMovePic / self.DELAY_FACTOR)
        return pygame.image.load( 'images/' + self.animFolder + '/move_left' + str(showpic) + '.gif' )

    #move right animation
    #delay anim to make it visible
    def __move_right(self):
        self.rightMovePic = (self.rightMovePic- 1) % (2*self.NUM_MOVEPICS)
        showpic = (int) (self.rightMovePic / 2)
        return pygame.image.load( 'images/' + self.animFolder + '/move_right' + str(showpic) + '.gif' )

class CaptainAmerica(Player):
    NUM_MOVEPICS = 4        #number pics in move anim
    DELAY_FACTOR = 2        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'america'


class Hulk(Player):
    NUM_MOVEPICS = 4        #number pics in move anim
    DELAY_FACTOR = 2        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 25     #xcoord movement velocity
    jumpVel = 35    #jumping velocity

    animFolder = 'hulk'

class IronMan(Player):
    NUM_MOVEPICS = 4        #number pics in move anim
    DELAY_FACTOR = 5        #delay factor to make anims visible
    leftMovePic = 7         #current move anim
    rightMovePic = 0         #current move anim

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'ironman'
