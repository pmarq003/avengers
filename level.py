import pygame
import pygame.sprite
import player
import levelobject
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Level(object):
    _terrain = pygame.sprite.Group()

    def update(self):
        self.player.update()

        #Make sure player doesn't go above or below map. Remember y-axis goes down
        if self.player.rect.bottom > self.height:
            self.player.rect.bottom = self.height
            self.player.stallY()
            self.player.canJump = True
        elif self.player.rect.top < 0:
            self.player.rect.top = 0
            self.player.stallY()


        collidedTerrain = pygame.sprite.spritecollide(self.player,self._terrain,False)
        #detect terrain collisions
        for ter in collidedTerrain:

            #check for a possible overlap situation
            if ((self.player.rect.bottom > ter.rect.top and self.player.velY > 0 ) and ( #detect down overlap
                (self.player.rect.left < ter.rect.right and
                    not self.player.rect.right > ter.rect.right) or
                (self.player.rect.right > ter.rect.left and
                    not self.player.rect.left > ter.rect.right))) or (
                (self.player.rect.top < ter.rect.bottom and self.player.velY < 0) and ( #detect up overlap
                (self.player.rect.left < ter.rect.right or
                    self.player.rect.right > ter.rect.left))) or (
                (self.player.rect.right > ter.rect.left and self.player.velX > 0) and ( #detect right overlap
                (self.player.rect.bottom > ter.rect.top and
                    not self.player.rect.top > ter.rect.bottom) or
                (self.player.rect.top < ter.rect.bottom and
                    not self.player.rect.bottom < ter.rect.top))) or (
                (self.player.rect.left < ter.rect.right and self.player.velX < 0) and ( #detect left overlap
                (self.player.rect.bottom > ter.rect.top and
                    not self.player.rect.top > ter.rect.bottom) or
                (self.player.rect.top < ter.rect.bottom and
                    not self.player.rect.bottom < ter.rect.top)
                )):
                    #sentinel overlap values
                    topOverlap = -500
                    botOverlap = 500
                    leftOverlap = -500
                    rightOverlap = 500
                    #check for the actual overlaps
                    #from the perspective of the player
                    if(self.player.rect.top - ter.rect.bottom < 0):
                        topOverlap = self.player.rect.top - ter.rect.bottom
                    if(self.player.rect.bottom - ter.rect.top > 0):
                        botOverlap = self.player.rect.bottom- ter.rect.top
                    if(self.player.rect.left - ter.rect.right < 0):
                        leftOverlap = self.player.rect.left - ter.rect.right
                    if(self.player.rect.right - ter.rect.left > 0):
                        rightOverlap = self.player.rect.right - ter.rect.left

                    #correct only the smallest overlap
                    if min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(topOverlap):
                        self.player.stallY()
                        self.player.rect.top = ter.rect.bottom
                    elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == botOverlap:
                        self.player.stallY()
                        self.player.canJump = True
                        self.player.rect.bottom = ter.rect.top
                    elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(leftOverlap):
                        self.player.stallX()
                        self.player.rect.left = ter.rect.right
                    elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == rightOverlap:
                        self.player.stallX()
                        self.player.rect.right = ter.rect.left


    def draw(self,camera):
        if self.background:
            self.background.draw(camera)
        self.player.draw(camera)

        for terrainObj in self._terrain:
            terrainObj.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

    def _addTerrain(self,terrainObj):
        self._terrain.add(terrainObj)


class Level1(Level):

    def __init__(self):
        self.height = SCREEN_HEIGHT
        self.player = player.Hulk(0,0)

        #TODO do some smart screen scrolling here later
        #bg = pygame.image.load("images/backgrounds/bg1.gif").convert_alpha()
        #for x in range(0, 3000, 1918):
        #    self.blit( bg,(x,0))
        self.background = levelobject.StaticImage('images/300x300logo.jpg',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

        self._addTerrain( levelobject.BasicPlatform(100,400) )
        self._addTerrain( levelobject.BasicPlatform(500,500) )
        self._addTerrain( levelobject.BasicPlatform(900,300) )
