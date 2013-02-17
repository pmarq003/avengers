from character import Character
import eventmanager

class Player(Character):

    def charSpecificUpdate(self):

        evman = eventmanager.get()
        if evman.NORMPRESSED:                   #normal attack pressed
            self.attack = True
            if(self.velY != 0):
                self._load_image( self.jump_attack )
            else:
                self.stallX()
                self._load_image( self.norm_attack )
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
