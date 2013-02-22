from character import Character
import eventmanager
import pygame.mixer

class Player(Character):
    can_get_hurt  = True
    can_give_hurt = True

    def charSpecificUpdate(self):

        evman = eventmanager.get()

        if evman.LEFTPRESSED: #left key pressed
            self.velX = -self.runVel
            self.facingRight = False
            self._load_image( self.walk )

        elif evman.RIGHTPRESSED: #right key pressed
            self.velX = self.runVel
            self.facingRight = True
            self._load_image( self.walk )

        else:
            self.velX = 0
            if not self.isJumping:
                self._load_image( self.stand )

        if self.isJumping:
            self._load_image( self.jump )

        #jumping upwards
        elif evman.SPACEPRESSED and not self.attacking:
            self.isJumping = True
            self.velY -= self.jumpVel
            self._load_image( self.jump )

        if evman.NORMPRESSED:                   #normal attack pressed
            self.attacking = True
            pygame.mixer.Sound("sounds/SSB_Kick_Hit1.wav").play()
            if self.isJumping:
                self._load_image( self.jump_attack )
            else:
                self.stallX()
                self._load_image( self.norm_attack )

        else:
            self.attacking = False

    def got_hurt(self,by):
        self.die()

class CaptainAmerica(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'america'


class Hulk(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 25     #xcoord movement velocity
    jumpVel = 35    #jumping velocity

    animFolder = 'hulk'

class IronMan(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 5        #delay factor to make anims visible

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'ironman'

class Thor(Player):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 20     #xcoord movement velocity
    jumpVel = 20    #jumping velocity

    animFolder = 'thor'
