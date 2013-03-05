import charsel
import pygame
import pygame.sprite
import player
import enemy
import levelobject
from constants import *
from levelobject import LevelObject,StaticImage
import eventmanager
import startmenu
import sound

"""
    level.py
            holds player collision detection
            to see AI nodes uncomment line 183-184
            AI constants can be found in constants.py
            levels found at bottom of file
"""

class Level(object):

    def __init__(self):
        self.levelNumber = -1   #override in specific levels
        self.charsel = charsel.CharSel()
        self.charSelected = False
        self._terrain = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()
        self._nodes = pygame.sprite.Group()
        self._entities = pygame.sprite.Group()
        self._checkpoints = []

        self.vol = True

        self.player_alive = True

    def update(self):

        if not self.charSelected:
            self.charsel.update()
            choice = self.charsel.getChar()
            if choice == 1:
                self.player = player.Hulk(0,500,self)
            elif choice == 2:
                self.player = player.Thor(0,500,self)
            elif choice == 3:
                self.player = player.CaptainAmerica(0,500,self)
            elif choice == 4:
                self.player = player.IronMan(0,500,self)
            elif choice == 5:
                self.player = player.Hawkeye(0,500,self)
            elif choice == 6:
                self.player = player.BlackWidow(0,500,self)

            if choice > 0 : self.charSelected = True

        else:

            #update player
            self.player.update()
            #update enemies
            for enemyObj in self._enemies:
                enemyObj.update()
            #update entities
            for entObj in self._entities:
                entObj.update()
            #update terrain
            for terr in self._terrain:
                terr.update()

            #Make sure player doesn't go below map. Remember y-axis goes down
            #If the player goes below we assume they're dead
            if self.player.rect.top > self.height:
                print("player dead")
                self.player.kill()
                self.player_alive = False

            if self.player.rect.left < 0:
                self.player.rect.left = 0

            #Make sure enemy doesn't go below map. Remember y-axis goes down
            #If the enemy goes below we assume they're dead
            for enemyObj in self._enemies:
                if enemyObj.rect.top > self.height:
                    enemyObj.kill() #removes from all sprite groups

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
            for enemy,terObjs in enemyTerrainCollisions.items():
                for ter in terObjs:
                    self._handleCollision(enemy,ter)

            enemyEntityCollisions = pygame.sprite.groupcollide(self._enemies,self._entities,False,False)
            for enemy,entObjs in enemyEntityCollisions.items():
                for ent in entObjs:
                    enemy.try_hurt(ent)
                    if ent.kill_on_collide:
                        ent.kill()

            #detect AI nodes for enemies
            enemyNodeCollisions = pygame.sprite.groupcollide(self._enemies,self._nodes,False,False)
            for enemy,nodeObjs in enemyNodeCollisions.items():
                for node in nodeObjs:
                    self._handleNodeCollision(enemy,node)

            #detect AI nodes for terrain
            terrNodeCollisions = pygame.sprite.groupcollide(self._terrain,self._nodes,False,False)
            for terr,nodeObjs in terrNodeCollisions.items():
                for node in nodeObjs:
                    self._handleNodeCollision(terr,node)

            #player / checkpoint collisions
            i = 0
            while i < len(self._checkpoints) :
                if self.player.rect.x > self._checkpoints[i]:
                    #remove previous checkpoints
                    self._checkpoints.remove( self._checkpoints[i] )
                    i -= 1
                    #save state
                    self.saveLevel()
                i += 1


    def _handleNodeCollision(self, enemy, node):
        enemy.handleNodeCollision(node);

    def _handleCollision(self,a,b):

        #If either object isn't solid we don't care
        if not a.solid or not b.solid: return

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
            a.isJumping = False
            a.rect.bottom = b.rect.top
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(leftOverlap):
            a.stallX()
            a.rect.left = b.rect.right
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == rightOverlap:
            a.stallX()
            a.rect.right = b.rect.left

        b.try_hurt(a)


    def draw(self,camera):

        if not self.charSelected:
            self.charsel.draw(camera)
        else:
            if self.background:
                self.background.draw(camera)
            self.player.draw(camera)

            #update '-30' to width of the volume image
            self.volume_button = StaticImage( "images/menusprites/volume.png",
                    camera.window.right-30, camera.window.top )
            self.mute_button = StaticImage( "images/menusprites/mute.png",
                    camera.window.right-30, camera.window.top )

            for terrainObj in self._terrain:
                terrainObj.draw(camera)

            for enemyObj in self._enemies:
                enemyObj.draw(camera)

            for entObj in self._entities:
                entObj.draw(camera)

            #TODO uncomment for debugging
            for nodeObj in self._nodes:
                nodeObj.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

    def get_player(self):
        return self.player

    def _addTerrain(self,terrainObj):
        self._terrain.add(terrainObj)

    def _addEnemy(self,enemyObj):
        self._enemies.add(enemyObj)

    def _addNode(self, nodeObj):
        self._nodes.add(nodeObj);

    def _addCheckpoint(self, x):
        self._checkpoints.append(x)

    def addEntity(self, entObj):
        self._entities.add(entObj)

    def saveLevel(self):
        f = open('save', 'w')
        f.write( str(self.levelNumber) +
                " " + str( self.charsel.getChar() ) +
                " " + str( self.player.rect.x ) +
                " " + str( self.player.rect.y ) )
        f.close()

"""
    Tutorial level
"""

class Level0(Level):
    None

"""
    Mario level
"""

class Level1(Level):

    def __init__(self):
        Level.__init__(self)

        #level number
        self.levelNumber = 1

        self.height = SCREEN_HEIGHT
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/ToughGuy.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/smw/background.png',0,-55)

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-16) )
        self._addCheckpoint(0)
            #goombas
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.Goomba(500,400, self.player, PLATFORM) )
        self._addEnemy( enemy.Goomba(700,400, self.player, PLATFORM) )
        self._addEnemy( enemy.Goomba(900,400, self.player, PLATFORM) )
        self._addEnemy( enemy.Goomba(1100,400, self.player, PLATFORM) )
        self._addEnemy( enemy.Goomba(1300,400, self.player, PLATFORM) )
        self._addNode( levelobject.Node(1500,550) )
            #ParaKoopa
        self._addNode( levelobject.Node(1700, 200) )
        self._addEnemy( enemy.ParaKoopa(1700,400, self.player, FLYVERT) )
        self._addNode( levelobject.Node(1700, 500) )
        self._addTerrain( levelobject.MarioPlatform6(1750,400) )
            #ParaKoopa
        self._addNode( levelobject.Node(2000, 0) )
        self._addEnemy( enemy.ParaKoopa(2000,300, self.player, FLYVERT) )
        self._addNode( levelobject.Node(2000, 400) )
        self._addTerrain( levelobject.MarioPlatform6(2050,200) )
            #empty platform
        self._addTerrain( levelobject.MarioPlatform6(2350,350) )
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(2600,SCREEN_HEIGHT-16) )
        self._addCheckpoint(2700)
            #enemies
        self._addEnemy( enemy.Fuzzy(2900, 500, self.player, HOP) )
        self._addEnemy( enemy.ParaKoopa(3100, 150, self.player, FLYSWOOP) )
        self._addEnemy( enemy.Fuzzy(3150, 500, self.player, HOP) )
        self._addTerrain( levelobject.MarioPlatform6(3200,400) )
        self._addEnemy( enemy.Fuzzy(3400, 500, self.player, HOP) )
        self._addEnemy( enemy.Fuzzy(3600, 500, self.player, HOP) )
        self._addEnemy( enemy.Fuzzy(3800, 500, self.player, HOP) )
        self._addEnemy( enemy.Fuzzy(4000, 500, self.player, HOP) )
            #mushroom platforms
        self._addTerrain( levelobject.MarioMushroomPlatform(4450,500) )
        self._addEnemy( enemy.Fuzzy(4470, 500, self.player, JUMP) )
        self._addTerrain( levelobject.MarioMushroomPlatform(4700,300) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(4716,400) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(4716,502) )
        self._addEnemy( enemy.Fuzzy(4720, 300, self.player, JUMP) )
        self._addTerrain( levelobject.MarioMushroomPlatform(5000,300) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(5016,400) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(5016,502) )
        self._addEnemy( enemy.Fuzzy(5050, 300, self.player, JUMP) )
            #movable platform + enemies on clouds
        self._addNode( levelobject.Node(5200,300,0,0,-1))
        self._addTerrain( levelobject.MarioMovablePlatform(5400,300, 5) )
        self._addTerrain( levelobject.MarioCloud(5600,200) )
        self._addEnemy( enemy.Fuzzy(5660, 100, self.player, JUMP) )
        self._addTerrain( levelobject.MarioCloud(6200,200) )
        self._addEnemy( enemy.Fuzzy(6260, 100, self.player, JUMP) )
        self._addNode( levelobject.Node(6700,300,0,0,-1))
            #checkpoint
        self._addCheckpoint(6800)
            #platforms w shyguy
        self._addNode( levelobject.Node(6800,180) )
        self._addTerrain( levelobject.MarioPlatform12(6800,200) )
        self._addEnemy( enemy.ShyGuy(6970, 180, self.player, PLATFORM) )
        self._addNode( levelobject.Node(7174,180) )
            #vertical platform
        self._addNode( levelobject.Node(7300,180,0,0,0,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(7300,100,0,5) )
        self._addNode( levelobject.Node(7300,-500,0,0,0,-1) )
            #clouds + koopas
        self._addTerrain( levelobject.MarioCloud(7510, -500))
        self._addTerrain( levelobject.MarioCloud(7800, -200) )
        self._addNode( levelobject.Node(7830, -300) )
        self._addEnemy( enemy.ParaKoopa(7830,-600, self.player, FLYVERT) )
        self._addNode( levelobject.Node(7830, -600) )
        self._addTerrain( levelobject.MarioCloud(7870, -720) )
        self._addEnemy( enemy.ParaKoopa(7800,-950, self.player, FLYSWOOP) )
        self._addTerrain( levelobject.MarioCloud(8100, -400) )
            #two koopas in between two clouds
        self._addTerrain( levelobject.MarioCloud(8400,-600) )
        self._addNode( levelobject.Node(8600, -500) )
        self._addEnemy( enemy.ParaKoopa(8600,-994, self.player, FLYVERT) )
        self._addNode( levelobject.Node(8600, -1000) )
        self._addNode( levelobject.Node(8750, -500) )
        self._addEnemy( enemy.ParaKoopa(8750,-583, self.player, FLYVERT) )
        self._addNode( levelobject.Node(8750, -1000) )
        self._addTerrain( levelobject.MarioCloud(8850,-600) )
            #two koopas in between two clouds
        self._addTerrain( levelobject.MarioCloud(9200,-700) )
        self._addNode( levelobject.Node(9400, -600) )
        self._addEnemy( enemy.ParaKoopa(9400,-1094, self.player, FLYVERT) )
        self._addNode( levelobject.Node(9400, -1100) )
        self._addNode( levelobject.Node(9550, -600) )
        self._addEnemy( enemy.ParaKoopa(9550,-683, self.player, FLYVERT) )
        self._addNode( levelobject.Node(9550, -1100) )
        self._addTerrain( levelobject.MarioCloud(9650,-700) )
            #platform back to ground

"""
    Sonic level
"""

class Level2(Level):

    def __init__(self):
        Level.__init__(self)

        #level number
        self.levelNumber = 2

        self.height = SCREEN_HEIGHT
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/ToughGuy.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/sonic/background.jpg',0,-55)

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioPlatform6(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)

"""
    Megaman level
"""

class Level3(Level):

    def __init__(self):
        Level.__init__(self)

        #level number
        self.levelNumber = 3

        self.height = SCREEN_HEIGHT
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/ToughGuy.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/megaman/background.png',0,-55)

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioPlatform6(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)

