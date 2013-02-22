from levelobject import LevelObject
from character import Character
from constants import *
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from pygame.sprite import Sprite

import random


class Enemy(Character):
    can_get_hurt  = True
    can_give_hurt = True

    def charSpecificUpdate(self):
        if(self.velY == 0):
            self._load_image( self.stand )

    def got_hurt(self,by):
        if by.attacking:
            self.die()
        elif by.can_get_hurt:
            by.die()

    def __init__(self, x, y, player, ai):
        #general stuff
        self.isJumping = False   #used to detect the peak of player's jump
        self.peaking = False     #is player at the peak of its jump?
        self.isFlying = False   #is the player flying?
        self.facingRight = True  #player facing right?
        self.attacking = False   #player attacking?
        self.canMove = False
        self.canJump = False
        self.velX = 0
        self.velY = 0
        self.player = player
        self.ai = ai

        #choose AI to implement
        self.AI_implementations = { NONE:     self.AI_nothing,
                                    FLOOR:    self.AI_floor,
                                    PLATFORM: self.AI_platform,
                                    JUMP:     self.AI_jump,
                                    HOP:      self.AI_hop,
                                    FLYVERT:  self.AI_flyvert,
                                    FLYSWOOP: self.AI_flyswoop }

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
        #self.__load_image( self.stand )

        self.AI_implementations[self.ai]()

        #update rect with new image
        #we use bottomleft so it doesn't mess with collision detection
        oldxy = self.rect.bottomleft
        self.rect = self.anim.get_rect()
        self.rect.bottomleft = oldxy

        #gravity
        if not self.isFlying:
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

    """
    AI
    """

    #0: NONE - AI for enemy that does nothing
    def AI_nothing(self):
        pass

    #1: FLOOR - AI for enemy that runs only on floor, following the player
    def AI_floor(self):
        #checks player radius
        if self.rect.left - self.player.rect.left <= self.playerRadius:
            self.canMove = True

        if self.velX == 0:
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

    #2: PLATFORM - AI for enemes that patrol a platform
    def AI_platform(self):

        if self.facingRight == True:
            self.velX = self.runVel / 2
            self.__load_image( self.walk )
        elif self.facingRight == False:
            self.velX = -self.runVel / 2
            self.__load_image( self.walk )
        else:
            self.__load_image( self.stand )

    #3: JUMP - AI for static jumping enemies
    def AI_jump(self):

        #set character orientation
        if(self.player.rect.left > self.rect.right):
            self.facingRight = True
        elif(self.player.rect.right < self.rect.left):
            self.facingRight = False

        #character is ready to jump again
        if self.canJump:
            #random chance to jump again
            if random.random() < 0.05:
                self.canJump = False
                self.isJumping = True
                self.velY -= self.jumpVel
                self.__load_image( self.jump )
            else:
                self.__load_image( self.stand )
        #enemy has reached peak
        elif self.velY == 0 and self.isJumping:
            self.isJumping = False
        #enemy has reached floor
        elif self.velY == 0 and not self.isJumping:
            self.canJump = True

    #4: HOP - hop, like a rabbit
    def AI_hop(self):

        #character is ready to jump again
        if self.canJump:
            #random chance to jump again
            if random.random() < 0.10:
                self.canJump = False
                self.isJumping = True
                self.velY -= self.jumpVel
                #small chance to reverse direction
                if random.random() < 0.15:
                    self.facingRight = not self.facingRight
                #move left or right to hop
                if self.facingRight:
                    self.velX = self.runVel / 2
                else:
                    self.velX = -self.runVel / 2
                self.__load_image( self.jump )
            else:
                self.__load_image( self.stand )
        #enemy has reached peak
        elif self.velY == 0 and self.isJumping:
            self.isJumping = False
        #enemy has reached floor
        elif self.velY == 0 and not self.isJumping:
            self.canJump = True

    #5: FLYVERT - fly up and down only
    def AI_flyvert(self):
        #self.peaking keeps track of up or down movement

        #negate gravity
        self.isFlying = True
        #set character orientation
        if(self.player.rect.left > self.rect.right):
            self.facingRight = True
        elif(self.player.rect.right < self.rect.left):
            self.facingRight = False
        #going up
        if not self.peaking:
            self.velY = self.jumpVel
            self.currentDist = self.currentDist + 1
            #hit top of vertical distance
            if self.currentDist == self.vertDist:
                self.peaking = True
        #going down
        elif self.peaking:
            self.velY = -self.jumpVel
            self.currentDist = self.currentDist - 1
            #hit bottom of vertical distance
            if self.currentDist <= 0:
                self.peaking = False

        self.__load_image( self.walk )

    #6: FLYSWOOP - fly in a parabola
    def AI_flyswoop(self):
        #self.isJumping keeps track of left or right movement
        #self.peaking keeps track of up or down movement

        #negate gravity
        self.isFlying = True
        #going left
        if not self.isJumping:
            self.facingRight = True
            self.velX = self.runVel
            self.currentDist = self.currentDist + 1
            #going down
            if not self.peaking:
                self.velY = self.jumpVel
                #hit bottom of parabola
                if self.currentDist == self.horizRadius / 2:
                    self.peaking = True
            #going up
            elif self.peaking:
                self.velY = -self.jumpVel
                #hit end of parabola
                if self.currentDist == self.horizRadius:
                    self.peaking = False
                    self.isJumping = True
        #going right
        if self.isJumping:
            self.facingRight = False
            self.velX = -self.runVel
            self.currentDist = self.currentDist - 1
            #going down
            if not self.peaking:
                self.velY = self.jumpVel
                #hit bottom of parabola
                if self.currentDist == self.horizRadius / 2:
                    self.peaking = True
            #going up
            elif self.peaking:
                self.velY = -self.jumpVel
                #hit end of parabola
                if self.currentDist == 0:
                    self.peaking = False
                    self.isJumping = False

        self.__load_image( self.walk )

    """
    AI Node Collision
    """

    #handles specific AI interactions with nodes in level
    def handleNodeCollision(self, node):
        if self.ai == PLATFORM:
            if self.facingRight:
                self.rect.right = node.rect.left
            else:
                self.rect.left = node.rect.right
            self.facingRight = not self.facingRight

    """
    Image population
    """

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



class CaptainRussia(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'captnrussia'

"""
Mario-themed enemies
"""

class Goomba(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'goomba'

class Mario(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'mario'

class Luigi(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 20    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'luigi'

class Fuzzy(Enemy):
    numWalkFrames = 1        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'fuzzy'

class RedKoopa(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'redkoopa'

class ParaKoopa(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 4    #jumping velocity

    #for FLYVERT
    vertDist = 40       #increase for longer vertical distance
    currentDist = 0     #KEEP ZERO
    #for FLYSWOOP
    horizRadius = 60    #increase for wider swoop
    currentHoriz = 0

    #distance before detect player
    playerRadius = 500

    animFolder = 'parakoopa'

class ShyGuy(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'shyguy'
