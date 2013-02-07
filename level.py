import pygame
import pygame.sprite
import player
import image
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
        for ter in collidedTerrain:
            #THIS SHIT DOES NOT WORK
            if self.player.rect.bottom <= ter.rect.top:
                if self.player.velX > 0:
                    self.player.stallX()
                    self.player.rect.right = ter.rect.left

                if self.player.velX < 0:
                    self.player.stallX()
                    self.player.rect.left = ter.rect.right

            #if self.player.rect.right <= ter.rect.left:
            if self.player.velY > 0:
                self.player.stallY()
                self.player.canJump = True
                self.player.rect.bottom = ter.rect.top

            if self.player.velY < 0:
                self.player.stallY()
                self.player.rect.top = ter.rect.bottom

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
        self.player = player.CaptainAmerica(0,0)
        self.background = image.StaticImage('images/300x300logo.jpg',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

        self._addTerrain( levelobject.BasicPlatform(100,500) )
