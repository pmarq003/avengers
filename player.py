from character import Character
import eventmanager
import pygame.mixer

class Player(Character):
    can_get_hurt  = True
    can_give_hurt = True

    def charSpecificUpdate(self):

        evman = eventmanager.get()
        self.attacking = False
        if evman.NORMPRESSED:                   #normal attack pressed
            self.attacking = True
            if(self.velY != 0):
                self._load_image( self.jump_attack )
            else:
                self.stallX()
                self._load_image( self.norm_attack )
            pygame.mixer.Sound("sounds/SSB_Kick_Hit1.wav").play()
        elif evman.LEFTPRESSED and self.rect.left > 5:      #left key pressed
            self.velX = -self.runVel
            self.facingRight = False
            if(self.velY == 0):
                self._load_image( self.walk )
        elif evman.RIGHTPRESSED:                #right key pressed
            self.velX = self.runVel
            self.facingRight = True
            if(self.velY == 0):
                self._load_image( self.walk )
        else:
            self.velX = 0
            if(self.velY == 0):
                self._load_image( self.stand )

        #jumping upwards
        if evman.SPACEPRESSED and self.canJump:
            self.isJumping = True
            self.canJump = False
            self.velY -= self.jumpVel
            self._load_image( self.jump )

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
