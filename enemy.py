from character import Character

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

class CaptainRussia(Enemy):
	numWalkFrames = 4        #number pics in move anim
	walkDelay = 2        #delay factor to make anims visible

	#movement vars
	runVel = 10     #xcoord movement velocity
	jumpVel = 25    #jumping velocity

	animFolder = 'captnrussia'
