import pygame
import pygame.sprite
import player
import enemy
import levelobject
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Level(object):
    _terrain = pygame.sprite.Group()
    _enemies = pygame.sprite.Group()

    def update(self):
        self.player.update()
        for enemyObj in self._enemies:
            enemyObj.update()

        #Make sure player doesn't go above or below map. Remember y-axis goes down
        if self.player.rect.bottom > self.height:
            self.player.rect.bottom = self.height
            self.player.stallY()
            self.player.canJump = True
        elif self.player.rect.top < 0:
            self.player.rect.top = 0
            self.player.stallY()
            
        #Make sure enemy doesn't go above or below map. Remember y-axis goes down
        #If the enemy goes below we assume they're dead
        for enemyObj in self._enemies:
            if enemyObj.rect.top > self.height:
                enemyObj.kill() #removes from all sprite groups
            elif enemyObj.rect.top < 0:
                enemyObj.rect.top = 0
                enemyObj.stallY()

        #detect terrain collisions for player
        collidedTerrain = pygame.sprite.spritecollide(self.player,self._terrain,False)
        for ter in collidedTerrain:
            self._handleCollision(self.player,ter)

        #detect enemy collisions for player
        collidedEnemies = pygame.sprite.spritecollide(self.player,self._enemies,False)
        for enemy in collidedEnemies:
            self._handleCollision(self.player,enemy)

        #detect terrain collisions for enemy
        enemyTerrainCollisions = pygame.sprite.groupcollide(self._enemies,self._terrain,False,False)
        for enemy,terObjs in enemyTerrainCollisions.iteritems():
            for ter in terObjs:
                self._handleCollision(enemy,ter)


    def _handleCollision(self,a,b):

        #If either object isn't solid we don't care
        if not a.solid or not b.solid: return

        b.try_hurt(a)

        #sentinel overlap values
        topOverlap = -500
        botOverlap = 500
        leftOverlap = -500
        rightOverlap = 500
        #check for the actual overlaps
        #from the perspective of the player
        if(a.rect.top - b.rect.bottom < 0):
            topOverlap = a.rect.top - b.rect.bottom
        if(a.rect.bottom - b.rect.top > 0):
            botOverlap = a.rect.bottom- b.rect.top
        if(a.rect.left - b.rect.right < 0):
            leftOverlap = a.rect.left - b.rect.right
        if(a.rect.right - b.rect.left > 0):
            rightOverlap = a.rect.right - b.rect.left

        #correct only the smallest overlap
        if min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(topOverlap):
            a.stallY()
            a.rect.top = b.rect.bottom
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == botOverlap:
            a.stallY()
            a.canJump = True
            a.rect.bottom = b.rect.top
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(leftOverlap):
            a.stallX()
            a.rect.left = b.rect.right
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == rightOverlap:
            a.stallX()
            a.rect.right = b.rect.left

    def draw(self,camera):
        if self.background:
            self.background.draw(camera)
        self.player.draw(camera)

        for terrainObj in self._terrain:
            terrainObj.draw(camera)
            
        for enemyObj in self._enemies:
            enemyObj.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

    def _addTerrain(self,terrainObj):
        self._terrain.add(terrainObj)

    def _addEnemy(self,enemyObj):
        self._enemies.add(enemyObj)

class Level1(Level):

    def __init__(self):
        self.height = SCREEN_HEIGHT
        self.player = player.Hulk(0,0)

        #TODO do some smart screen scrolling here later
        #bg = pygame.image.load("images/backgrounds/bg1.gif").convert_alpha()
        #for x in range(0, 3000, 1918):
        #    self.blit( bg,(x,0))
        self.background = levelobject.StaticImage('images/level5.jpg',-500,-350)

        self._addTerrain( levelobject.BasicPlatform(100,400) )
        self._addTerrain( levelobject.BasicPlatform(500,500) )
        self._addTerrain( levelobject.BasicPlatform(900,300) )
        self._addTerrain( levelobject.BasicPlatform2(1400,300) )
        self._addEnemy( enemy.CaptainRussia(600,0) )
        self._addEnemy( enemy.CaptainRussia(300,0) )
        self._addEnemy( enemy.CaptainRussia(100,0) )
        
#        for i in range(0,1000):
#            self._addTerrain( levelobject.MarioGround(16*i,SCREEN_HEIGHT-16) )

        self._addTerrain( levelobject.MarioPlatform(-500, SCREEN_HEIGHT-16) )

