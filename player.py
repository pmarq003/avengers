from character import Character
import eventmanager
import pygame.mixer

class Player(Character):
    can_get_hurt  = True
    can_give_hurt = True
    attack_timer = 0

    def charSpecificUpdate(self):

        evman = eventmanager.get()

        if evman.NORMPRESSED or self.attack_timer != 0: #normal attack pressed

            if self.isJumping:
                self._load_image( self.jump_attack )
            else:
                self._load_image( self.norm_attack )

            #mid attack
            if self.attack_timer > 1:
                self.attacking = True
                self.attack_timer -= 1
                self.velX = self.primary_attack_speed if self.facingRight else -1*self.primary_attack_speed

            #start recovery phase
            elif self.attack_timer == 1:
                self.attacking = False
                self.attack_timer = -1*self.primary_attack_recovery
                if not self.isJumping: self.stallX()

            #start attack
            elif self.attack_timer == 0:
                self.attacking = True
                self.attack_timer = self.primary_attack_length
                pygame.mixer.Sound("sounds/SSB_Kick_Hit1.wav").play()

            #mid recovery
            else:
                self.attacking = False
                self.attack_timer += 1
                if not self.isJumping: self.stallX()

        elif evman.LEFTPRESSED: #left key pressed
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

        #Attack animation overrides others
        if not self.attacking:
            if self.isJumping:
                self._load_image( self.jump )

            #jumping upwards
            elif evman.SPACEPRESSED:
                self.isJumping = True
                self.velY -= self.jumpVel
                self._load_image( self.jump )

    def got_hurt(self,by):
        self.die()

class CaptainAmerica(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 10     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'america'

    primary_attack_speed = 10
    primary_attack_length = 5
    primary_attack_recovery = 5


class Hulk(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 25     #xcoord movement velocity
    jumpVel = 35    #jumping velocity

    animFolder = 'hulk'

    primary_attack_speed = 10
    primary_attack_length = 5
    primary_attack_recovery = 5

class IronMan(Player):
    numWalkFrames = 4        #number pics in move anim
    walkDelay = 5        #delay factor to make anims visible

    #movement vars
    runVel = 7     #xcoord movement velocity
    jumpVel = 25    #jumping velocity

    animFolder = 'ironman'

    primary_attack_speed = 10
    primary_attack_length = 5
    primary_attack_recovery = 5

class Thor(Player):
    numWalkFrames = 5        #number pics in move anim
    walkDelay = 2        #delay factor to make anims visible

    #movement vars
    runVel = 20     #xcoord movement velocity
    jumpVel = 20    #jumping velocity

    animFolder = 'thor'

    primary_attack_speed = 10
    primary_attack_length = 5
    primary_attack_recovery = 5
