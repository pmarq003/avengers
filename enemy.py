from levelobject import LevelObject
from character import Character
from constants import *
from animation import Animation,StaticAnimation
from levelobject import LevelObject
from levelobject import TransientEntity
from pygame.sprite import Sprite

import random
import avengers
import score
import time


class Enemy(Character):
    can_get_hurt  = True
    can_give_hurt = True

    def got_hurt(self,by):
        if by.attacking:
            score.get().incScore(30)
            self.die()
        elif by.can_get_hurt:
            by.got_hurt(self)

    def __init__(self, x, y, ai, level=None):
        #general stuff
        self.isFlying = False   #is the player flying?
        self.facingRight = False #player facing right?
        self.peaking = False     #is player at the peak of its jump?
        self.canMove = False
        self.canJump = False
        self.player = None
        self.ai = ai
        #shooting timer
        self.sattack_timer = 0
        #level instance - pass if enemy interacts with level
        self.level = level

        #choose AI to implement
        self.AI_implementations = { NONE:       self.AI_nothing,
                                    FLOOR:      self.AI_floor,
                                    PLATFORM:   self.AI_platform,
                                    JUMP:       self.AI_jump,
                                    HOP:        self.AI_hop,
                                    FLYVERT:    self.AI_flyvert,
                                    FLYHORIZ:   self.AI_flyhoriz,
                                    FLYSWOOP:   self.AI_flyswoop,
                                    FLYATTACK:  self.AI_flyattack,
                                    RPROJ:      self.AI_rproj,
                                    RPROJSTAND: self.AI_rprojstand,
                                    SHY:        self.AI_shy,
                                    CUSTOM:     None}

        Character.__init__(self,x,y)

    #updates the players velocities and animations
    #orientation is used to track whether the character is facing left or right
    def charSpecificUpdate(self):
        #if(self.velY == 0):
        #    self._load_image( self.stand )

        if self.ai != CUSTOM:
            self.AI_implementations[self.ai]()
        else:
            self.customAI()

        #counteract gravity
        if self.isFlying and self.alive:
            self.velY -= 1

    def stallX(self):
        self.velX = 0

    def stallY(self):
        self.velY = 0

    def stall(self):
        self.stallX()
        self.stallY()

    #need to set the player because of loading/char select madness
    def setPlayer(self, player):
        self.player = player

    """
    AI
    """

    #0: NONE - AI for enemy that does nothing
    def AI_nothing(self):
        pass

    #1: FLOOR - AI for enemy that runs only on floor, following the player
    def AI_floor(self):
        #checks player radius
        if not self.canMove and abs(self.rect.left - self.player.rect.left) <= self.playerRadius:
            self.canMove = True

        if self.velX == 0:
            self._load_image( self.stand )

        if self.canMove:

            if(self.player.rect.left > self.rect.right):
                self.facingRight = True
                self.velX = self.runVel
                self._load_image( self.walk )
            elif(self.player.rect.right < self.rect.left):
                self.facingRight = False
                self.velX = -self.runVel
                self._load_image( self.walk )
            else:
                self.stallX()
                self._load_image( self.stand )

    #2: PLATFORM - AI for enemes that patrol a platform
    #   requires nodes for start and end points
    def AI_platform(self):

        if self.facingRight == True:
            self.velX = self.runVel / 2
            self._load_image( self.walk )
        elif self.facingRight == False:
            self.velX = -self.runVel / 2
            self._load_image( self.walk )
        else:
            self._load_image( self.stand )

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
                self._load_image( self.jump )
            else:
                self._load_image( self.stand )
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
                self._load_image( self.jump )
            else:
                self._load_image( self.stand )
        #enemy has reached peak
        elif self.velY == 0 and self.isJumping:
            self.isJumping = False
        #enemy has reached floor
        elif self.velY == 0 and not self.isJumping:
            self.canJump = True

    #5: FLYVERT - fly up and down only
    #   requires nodes to start and end points
    #   self.peaking keeps track of up or down movement
    def AI_flyvert(self):

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
        #going down
        elif self.peaking:
            self.velY = -self.jumpVel

        self._load_image( self.walk )

    #6: FLYHORIZ - fly left and right only
    #   requires nodes to start and end points
    #   self.peaking keeps track of right or left
    def AI_flyhoriz(self):
        #negate gravity
        self.isFlying = True

        if self.facingRight:
            self.velX = self.runVel
        else:
            self.velX = -self.runVel

        self._load_image( self.walk )

    #7: FLYSWOOP - fly in a parabola
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

        self._load_image( self.walk )

    #8: FLYATTACK - position enemy offscreen, then when player is in radius swoop down towards him/her
    def AI_flyattack(self):
        self.isFlying = True

        #checks player radius
        if not self.canMove and abs(self.rect.left - self.player.rect.left) <= self.playerRadius:
            self.canMove = True

        if self.velX == 0:
            self._load_image( self.walk )

        if self.canMove:

            #update direction facing
            if(self.player.rect.left > self.rect.right):
                self.facingRight = True
            elif(self.player.rect.right < self.rect.left):
                self.facingRight = False

            #vector to player
            velx = self.player.rect.x - self.rect.x
            vely = self.player.rect.y - self.rect.y

            #prevent division by zero in next step
            if velx == 0:
                self.velx = -1

            #scale speed - make enemy twice as fast for kicks
            self.velX = 2 * self.runVel * velx*velx / (velx*velx + vely*vely)
            self.velY = 2 * self.runVel * vely*vely / (velx*velx + vely*vely)

            #correct for facing left
            if not self.facingRight:
                self.velX = self.velX * -1

            #correct for player above enemy
            if self.player.rect.y < self.rect.y:
                self.velY = self.velY * -1

            self._load_image( self.walk )

    #9 RPROJ - randomly shoot projectiles and follow player
    def AI_rproj(self):
        #checks player radius
        if not self.canMove and abs(self.rect.left - self.player.rect.left) <= self.playerRadius:
            self.canMove = True

        if self.velX == 0:
            self._load_image( self.walk )

        if self.canMove:

            #update direction facing
            if(self.player.rect.left > self.rect.right):
                self.facingRight = True
            elif(self.player.rect.right < self.rect.left):
                self.facingRight = False

            #shoot
            if self.sattack_timer == 0 and random.random() < 0.025:
                self.sattack_timer = 5
                self._load_image( self.norm_attack )
                self.stallX()
                if self.facingRight:
                    entity = self.ProjectileRight(0,0)
                    entity.rect.topleft = self.rect.topright
                    self.level.addEntity(entity)
                else:
                    entity = self.ProjectileLeft(0,0)
                    entity.rect.topright = self.rect.topleft
                    self.level.addEntity(entity)

            #else move
            elif self.sattack_timer == 0:
                if self.facingRight:
                    self.velX = self.runVel
                    self._load_image( self.walk )
                else:
                    self.velX = -self.runVel
                    self._load_image( self.walk )

            #else load attack image
            else:
                self.sattack_timer = self.sattack_timer - 1
                self._load_image( self.norm_attack )

    #10 RPROJSTAND - randomly shoot projectiles while standing still
    def AI_rprojstand(self):
        #checks player radius
        if not self.canMove and abs(self.rect.left - self.player.rect.left) <= self.playerRadius:
            self.canMove = True

        if self.velX == 0:
            self._load_image( self.walk )

        if self.canMove:

            #update direction facing
            if(self.player.rect.left > self.rect.right):
                self.facingRight = True
            elif(self.player.rect.right < self.rect.left):
                self.facingRight = False

            #shoot
            if self.sattack_timer == 0 and random.random() < 0.020:
                self.sattack_timer = 5
                self._load_image( self.norm_attack )
                self.stallX()
                if self.facingRight:
                    entity = self.ProjectileRight(0,0)
                    entity.rect.topleft = self.rect.topright
                    self.level.addEntity(entity)
                else:
                    entity = self.ProjectileLeft(0,0)
                    entity.rect.topright = self.rect.topleft
                    self.level.addEntity(entity)

            #else move
            elif self.sattack_timer == 0:
                self._load_image( self.stand )

            #else load attack image
            else:
                self.sattack_timer = self.sattack_timer - 1
                self._load_image( self.norm_attack )

    #11 SHY - won't chase player unless facing
    def AI_shy(self):
        self.isFlying = True

        #update direction facing
        if(self.player.rect.left > self.rect.right):
            self.facingRight = True
        elif(self.player.rect.right < self.rect.left):
            self.facingRight = False

        #vector to player
        velx = self.player.rect.x - self.rect.x
        vely = self.player.rect.y - self.rect.y

        #prevent division by zero in next step
        if velx == 0:
            self.velx = -1

        #scale speed 
        self.velX = self.runVel * velx*velx / (velx*velx + vely*vely)
        self.velY = self.runVel * vely*vely / (velx*velx + vely*vely)

        #correct for facing left
        if not self.facingRight:
            self.velX = self.velX * -1

        #correct for player above enemy
        if self.player.rect.y < self.rect.y:
            self.velY = self.velY * -1

        #player facing enemy - don't move
        if (self.facingRight and not self.player.facingRight) or (not
                self.facingRight and self.player.facingRight):
            self._load_image( self.stand )
            self.velX = 0
            self.velY = 0
        else:
            self._load_image( self.walk )


    """
    AI Node Collision - give actions when a specific AI hits a node
    """

    #handles specific AI interactions with nodes in level
    def handleNodeCollision(self, node):
        #tells platform AI to change direction
        if self.ai == PLATFORM:
            if self.facingRight:
                self.rect.right = node.rect.left
            else:
                self.rect.left = node.rect.right
            self.facingRight = not self.facingRight
        #can be used to stop AI from hopping off a cliff
        elif self.ai == HOP:
            self.velX *= node.xmult
            self.facingRight = not self.facingRight
        #tells flying AI to change directions
        elif self.ai == FLYVERT:
            self.peaking = not self.peaking

        elif self.ai == FLYHORIZ:
            if self.facingRight:
                self.rect.right = node.rect.left
            else:
                self.rect.left = node.rect.right
            self.facingRight = not self.facingRight
            self.velX *= -1


"""
Tutorial enemies
"""

class Kit1(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #harmless
    can_give_hurt = False

    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/kit1'

class Kit2(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible
    
    #harmless
    can_give_hurt = False

    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/kit2'

class Pup1(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #harmless
    can_give_hurt = False    
    
    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/pup1'

class Pup2(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #harmless
    can_give_hurt = False

    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/pup2'

class Pup3(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #harmless
    can_give_hurt = False

    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/pup3'

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
    playerRadius = 900

    animFolder = 'enemysprites/goomba'

class Mario(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 15     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 700

    animFolder = 'enemysprites/mario'

class Luigi(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 20     #xcoord movement velocity
    jumpVel = 20    #jumping velocity

    #distance before detect player
    playerRadius = 700

    animFolder = 'enemysprites/luigi'

class Fuzzy(Enemy):
    numWalkFrames = 1        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/fuzzy'

class RedKoopa(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/redkoopa'

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
    playerRadius = 1000

    animFolder = 'enemysprites/parakoopa'

class ShyGuy(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/shyguy'

class ShootingShyGuy(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/shootingshyguy'

    #projectile classes
    class ProjectileLeft(TransientEntity):
            attacking = False #True
            can_give_hurt = True
            kill_on_collide = True#True
            base_img_path = 'images/enemysprites/shootingshyguy/projectile_left.gif'
            timeout = 100

            def update(self):
                TransientEntity.update(self)
                self.rect.left -= 20

    class ProjectileRight(TransientEntity):
        attacking = False#True
        can_give_hurt = True
        kill_on_collide = True#True
        base_img_path = 'images/enemysprites/shootingshyguy/projectile_right.gif'
        timeout = 100

        def update(self):
            TransientEntity.update(self)
            self.rect.left += 20

class Boo(Enemy):
    numWalkFrames = 3
    walkDelay = 5

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/boo'

class BooFast(Enemy):
    numWalkFrames = 3
    walkDelay = 5

    #movement vars
    runVel = 9     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/boo'

"""
Sonic-themed enemies
"""

class Sonic(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 35     #xcoord movement velocity
    jumpVel = 5    #jumping velocity

    #distance before detect player
    playerRadius = 50

    animFolder = 'enemysprites/sonic'

class Robotnik(Enemy):
    numWalkFrames = 2        #number pics in move anim
    walkDelay = 5        #delay factor to make anims visible
    
    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 3    #jumping velocity
    
    #for FLYVERT
    vertDist = 5       #increase for longer vertical distance
    currentDist = 0     #KEEP ZERO
    #for FLYSWOOP
    horizRadius = 200    #increase for wider swoop
    currentHoriz = 0

    #distance before detect player
    playerRadius = 1000
    
    animFolder = 'enemysprites/robotnik'
    
class Chao(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible
    
    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity
    
    #distance before detect player
    playerRadius = 900
    
    animFolder = 'enemysprites/chao'
    
class Cream(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/cream'
    
class Gamma(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 15    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/gamma'

"""
Megaman-themed enemies
"""

class BoyRobot1(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/boyrobot1'
    
    #projectile classes
    class ProjectileLeft(TransientEntity):
            attacking = False #True
            can_give_hurt = True
            kill_on_collide = True#True
            base_img_path = 'images/enemysprites/shootingshyguy/projectile_left.gif'
            timeout = 100

            def update(self):
                TransientEntity.update(self)
                self.rect.left -= 20

    class ProjectileRight(TransientEntity):
        attacking = False#True
        can_give_hurt = True
        kill_on_collide = True#True
        base_img_path = 'images/enemysprites/shootingshyguy/projectile_right.gif'
        timeout = 100

        def update(self):
            TransientEntity.update(self)
            self.rect.left += 20

class BoyRobot2(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/boyrobot2'
    
    #projectile classes
    class ProjectileLeft(TransientEntity):
            attacking = False #True
            can_give_hurt = True
            kill_on_collide = True#True
            base_img_path = 'images/enemysprites/shootingshyguy/projectile_left.gif'
            timeout = 100

            def update(self):
                TransientEntity.update(self)
                self.rect.left -= 20

    class ProjectileRight(TransientEntity):
        attacking = False#True
        can_give_hurt = True
        kill_on_collide = True#True
        base_img_path = 'images/enemysprites/shootingshyguy/projectile_right.gif'
        timeout = 100

        def update(self):
            TransientEntity.update(self)
            self.rect.left += 20
    
class BoyRobot3(Enemy):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/boyrobot3'
    
    #projectile classes
    class ProjectileLeft(TransientEntity):
            attacking = False #True
            can_give_hurt = True
            kill_on_collide = True#True
            base_img_path = 'images/enemysprites/shootingshyguy/projectile_left.gif'
            timeout = 100

            def update(self):
                TransientEntity.update(self)
                self.rect.left -= 20

    class ProjectileRight(TransientEntity):
        attacking = False#True
        can_give_hurt = True
        kill_on_collide = True#True
        base_img_path = 'images/enemysprites/shootingshyguy/projectile_right.gif'
        timeout = 100

        def update(self):
            TransientEntity.update(self)
            self.rect.left += 20
    
class Drone(Enemy):
    numWalkFrames = 4        #number pics in move anim
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
    playerRadius = 200

    animFolder = 'enemysprites/drone'
    
    
"""
Metroid-themed enemies
"""

class SpacePirate(Enemy):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 5     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/spacepirate'

class Metroid(Enemy):
    isFlying = True
    numWalkFrames = 7        #number pics in move anim
    walkDelay = 5        #delay factor to make anims visible

    #movement vars
    runVel = 3     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/metroid'

class Ridley(Enemy):
    can_get_hurt = False #hard-mode
    numWalkFrames = 1        #number pics in move anim
    walkDelay = 5        #delay factor to make anims visible

    #movement vars
    runVel = 15     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/ridley'

    def __init__(self, x, y, ai, level=None):
        Enemy.__init__(self,x,y,ai,level)
        self.norm_attack = Animation('images/' + self.animFolder + '/norm_attack_left{0}.gif',  5, 5),\
						   Animation('images/' + self.animFolder + '/norm_attack_right{0}.gif', 5, 5)

    def customAI(self):
        playerDistance = abs(self.rect.left - self.player.rect.right)
        if playerDistance < 400:
            self._load_image( self.norm_attack )
            self.velX = -self.runVel
        else:
            self._load_image( self.stand )
            self.velX = 0

    
class FastMetroid(Metroid):
    runVel = 15
    
"""
Castlevania-themed enemies
"""

class Ghoul(Enemy):
    numWalkFrames = 1        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 20     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/ghoul'

class GhoulSlow(Enemy):
    numWalkFrames = 1        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 0    #jumping velocity

    #distance before detect player
    playerRadius = 500

    animFolder = 'enemysprites/ghoul'
