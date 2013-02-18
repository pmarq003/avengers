import pygame
import eventmanager
import logger
import levelobject
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite


EMPTY = 0
FLOOR = 1

class Enemy(LevelObject):

    def __init__(self, x, y, player, ai):
        #general stuff
        self.isJumping = False   #used to detect the peak of player's jump
        self.peaking = False     #is player at the peak of its jump?
        self.facingRight = True  #player facing right?
        self.attacking = False   #player attacking?
        self.canJump = False
        self.velX = 0
        self.velY = 0
        self.player = player
        self.ai = ai

        #load images and do rest of constructor
        self.__populate_image_variables()
        self.anim = None
        self.__load_image( self.stand )
        LevelObject.__init__(self,x,y)


    def __load_image( self, img_tuple ):
        left,right = img_tuple
        toset = None
        if self.facingRight: toset = right
        else:                toset = left

        if not toset == self.anim:
            toset.reset()
        self.anim = toset

    #updates the players velocities and animations
    #orientation is used to track whether the character is facing left or right
    def update(self):
        self.anim.update()
        self.__load_image( self.stand )

        #choose AI to implement
        updateAI = {EMPTY: self.AI_nothing, FLOOR: self.AI_floor}
        updateAI[self.ai]()

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
        self.norm_attack = StaticAnimation('images/' + animd + '/norm_attack_left.gif'),\
                           StaticAnimation('images/' + animd + '/norm_attack_right.gif')
        self.jump_attack = StaticAnimation('images/' + animd + '/jump_attack_left.gif'),\
                           StaticAnimation('images/' + animd + '/jump_attack_right.gif')
        #self.spec_attack = StaticAnimation(''),\
        #                   StaticAnimation('')
        self.fall        = StaticAnimation('images/' + animd + '/jump_left.gif'),\
                           StaticAnimation('images/' + animd + '/jump_right.gif')
        self.jump        = StaticAnimation('images/' + animd + '/jump_left.gif'),\
                           StaticAnimation('images/' + animd + '/jump_right.gif')
        self.jump_peak   = StaticAnimation('images/' + animd + '/jump_left.gif'),\
                           StaticAnimation('images/' + animd + '/jump_right.gif')
        self.stand       = StaticAnimation('images/' + animd + '/stand_left.gif'),\
                           StaticAnimation('images/' + animd + '/stand_right.gif')
        self.walk        = Animation('images/' + animd + '/move_left{0}.gif',  self.numWalkFrames, self.walkDelay ),\
                           Animation('images/' + animd + '/move_right{0}.gif', self.numWalkFrames, self.walkDelay )

    def AI_nothing(self):
        pass

    def AI_floor(self):
        #checks player radius
        if self.rect.left - self.player.rect.left <= self.playerRadius:
            self.canMove = True

        self.anim.update()
        self.__load_image( self.stand )

        if self.canMove:

            if(self.player.rect.left > self.rect.right):
                self.facingRight = True
                self.velX = self.runVel
                self.__load_image( self.walk )
            elif(self.player.rect.right < self.rect.left):
                self.facingRight = False
                self.velX = -self.runVel
                self.__load_image( self.walk )
            else:
                self.stallX()
                self.__load_image( self.stand )

        

class CaptainRussia(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'captnrussia'
