import pygame
import eventmanager
import logger
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite

class Character(LevelObject):
    alive = True

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
        self.anim = None
        self._load_image( self.stand )
        LevelObject.__init__(self,x,y)
    

    def _load_image( self, img_tuple ):
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

        #If we're not alive don't process anything
        if self.alive:

            evman = eventmanager.get()

            #replay
            if evman.REPLAYPRESSED and logger.get().replayCanRun:
                logger.get().replay()

            #Do any updates pertaining to the child character class.
            #If the child class hasn't implemented the method, don't worry about it
            try: self.charSpecificUpdate()
            except AttributeError: pass

            #downward falling animation
            if(self.velY > 0):
                self.isJumping = False
                self.canJump = False    #remove if you want to jump in midair while falling
                self._load_image( self.fall )

            #detect frame after peak jump 
            #show peak frame for consistency
            if(self.peaking):
                self.peaking = False
                self._load_image( self.jump_peak )

            #detect jump peak
            if(self.velY == 0 and self.isJumping):
                self.peaking = True
                self._load_image( self.jump_peak )

        #Oh snap gravity!
        self.velY += 1
        self.rect.move_ip(self.velX,self.velY)

    def die(self):
        self.velY = -15
        self.alive = False
        self.solid = False

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
