import charsel
import enemy
import eventmanager
import levelobject
import plot
import pygame
import pygame.sprite
import player
import physics
import score
import sound
import startmenu
from constants import *
from levelobject import LevelObject,StaticImage
from parallax import Parallax

import constants


"""
    level.py
            holds player collision detection
            to see AI nodes uncomment line 191-193ish
            AI constants can be found in constants.py
            levels found at bottom of file

            The level is COMPLETED when there are NO MORE CHECKPOINTS LEFT!
            Add a checkpoint at the end of the level!
"""

class Level(object):

    def __init__(self,gameObj):
        self.gameObj = gameObj #unfortunately we need this
        self.levelNumber = -100   #override in specific levels
        self.charsel = charsel.CharSel()
        self.charSelected = False
  #      self.plot = plot.Plot(-1)
        self.plotOver = True
        self._terrain = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()
        self._nodes = pygame.sprite.Group()
        self._entities = pygame.sprite.Group()
        self._hearts = pygame.sprite.Group()
        self._heart3s = pygame.sprite.Group()
        self._ammo = pygame.sprite.Group()
        self._ammo3 = pygame.sprite.Group()
        self._stars = pygame.sprite.Group()
        self._checkpoints = []
        #True when all checkpoints have been reached
        #put one checkpoint at end of level
        self.levelCompleted = False

        self.vol = True

        self.player_alive = True

    def setPlayer(self, choice, x = 0, y = 500):  # used for replay
        if choice == 1:
            self.player = player.Hulk(x,y,self)
        elif choice == 2:
            self.player = player.Thor(x,y,self)
        elif choice == 3:
            self.player = player.CaptainAmerica(x,y,self)
        elif choice == 4:
            self.player = player.IronMan(x,y,self)
        elif choice == 5:
            self.player = player.Hawkeye(x,y,self)
        elif choice == 6:
            self.player = player.BlackWidow(x,y,self)

        if choice > 0 : self.charSelected = True 

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

        elif not self.plotOver:
            self.plot.update()
            if self.plot.getPlot() : self.plotOver = True

        else:

            #update player
            self.player.update()
            #update enemies and give them the current player's status/coords
            for enemyObj in self._enemies:
                enemyObj.setPlayer(self.player)
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
                if self.player.has_star:
                    if enemy.alive:
                        score.get().incScore(30)
                    enemy.die()
                else:
                    self._handleEnemyCollision(self.player,enemy)

            #detect entity collisions for player
            collidedEnts = pygame.sprite.spritecollide(self.player,self._entities,False)
            for entObj in collidedEnts:
                if not self.player.has_star:
                    self.player.try_hurt(entObj)
                    if entObj.kill_on_collide:
                        entObj.kill()

            #detect terrain collisions for enemy
            enemyTerrainCollisions = pygame.sprite.groupcollide(self._enemies,self._terrain,False,False)
            for enemy,terObjs in enemyTerrainCollisions.items():
                for ter in terObjs:
                    self._handleCollision(enemy,ter)

            #detect entity collision for enemy
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

            #detect heart powerup collisions
            heartCollisions = pygame.sprite.spritecollide(self.player,self._hearts,False)
            for heart in heartCollisions:
                self.gameObj.player_lives += 1
                heart.kill()
                
            #detect heart3 powerup collisions
            heart3Collisions = pygame.sprite.spritecollide(self.player,self._heart3s,False)
            for heart3 in heart3Collisions:
                self.gameObj.player_lives += 3
                heart3.kill()

            #detect ammo powerup collisions
            ammoCollisions = pygame.sprite.spritecollide(self.player,self._ammo,False)
            for ammo in ammoCollisions:
                self.player.incAmmo()
                ammo.kill()
                
            #detect ammo3 powerup collisions
            ammo3Collisions = pygame.sprite.spritecollide(self.player,self._ammo3,False)
            for ammo3 in ammo3Collisions:
                self.player.incAmmo3()
                ammo3.kill()

            #detect star powerup collisions
            starCollisions = pygame.sprite.spritecollide(self.player,self._stars,False)
            for star in starCollisions:
                self.player.star()
                star.kill()

            #update parallax
            if self.parallax:
                self.parallax.update(self.player.rect.x, self.player.rect.y)

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

            #check if level is done
            if len(self._checkpoints) == 0:
                self.levelCompleted = True

    def _handleEnemyCollision(self,player,enemy):
        physics.get().handleCollision(player, enemy)

    def _handleNodeCollision(self, enemy, node):
        enemy.handleNodeCollision(node);

    def _handleCollision(self,a,b):
        physics.get().handleCollision(a, b)

    def draw(self,camera):

        if not self.charSelected:
            self.charsel.draw(camera)
        elif not self.plotOver:
            self.plot.draw(camera)
        else:

            #draw parallax if there is no background
            if self.background:
                self.background.draw(camera)
            if self.parallax:
                self.parallax.draw(camera)

            #update '-30' to width of the volume image
            self.volume_button = StaticImage( "images/menusprites/volume.png",
                    camera.window.right-30, camera.window.top )
            self.mute_button = StaticImage( "images/menusprites/mute.png",
                    camera.window.right-30, camera.window.top )

            for terrainObj in self._terrain:
                terrainObj.draw(camera)

            self.player.draw(camera)

            for enemyObj in self._enemies:
                enemyObj.draw(camera)

            for entObj in self._entities:
                entObj.draw(camera)

            #TODO uncomment for debugging
            #for nodeObj in self._nodes:
            #    nodeObj.draw(camera)

            for heartObj in self._hearts:
                heartObj.draw(camera)
                
            for heartObj in self._heart3s:
                heartObj.draw(camera)

            for ammoObj in self._ammo:
                ammoObj.draw(camera)
                
            for ammoObj in self._ammo3:
                ammoObj.draw(camera)

            for starObj in self._stars:
                starObj.draw(camera)


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

    def _addHeart(self,heartObj):
        self._hearts.add(heartObj)
        
    def _addHeart3(self,heartObj):
        self._heart3s.add(heartObj)

    def _addAmmo(self,ammoObj):
        self._ammo.add(ammoObj)
        
    def _addAmmo3(self,ammoObj):
        self._ammo3.add(ammoObj)
    
    def _addStar(self, starObj):
        self._stars.add(starObj)

    def saveLevel(self):
        f = open('save', 'w')
        f.write( str(self.levelNumber) +
                " " + str( self.charsel.getChar() ) +
                " " + str( self.player.rect.x ) +
                " " + str( self.player.rect.y ) )
        f.close()


"""
    Level -1: Nuri Level
"""

class LevelNeg1(Level):
     def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        self.levelNumber = -1

        self.height = SCREEN_HEIGHT
        #default player to init enemies 
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl-1.mp3'

        #background
        self.background = None
        self.parallax = None

            #player spawns here
        self._addTerrain( levelobject.MarioPipeDown(500, 450) )

            #floor
        self._addTerrain( levelobject.CastleFloor(0, SCREEN_HEIGHT-32) )

            #assorted boos before player spawn
        self._addEnemy( enemy.Boo(100,100,SHY) )
        self._addEnemy( enemy.BooFast(240,130,SHY) )
        self._addEnemy( enemy.BooFast(200,150,SHY) )
        self._addEnemy( enemy.Boo(330,0,SHY) )
            #boos after player spawn 
        self._addEnemy( enemy.BooFast(600,250,SHY) )
        self._addEnemy( enemy.BooFast(730,455,SHY) )
        self._addEnemy( enemy.Boo(800,300,SHY) )
        self._addEnemy( enemy.BooFast(890,450,SHY) )
        self._addEnemy( enemy.Boo(940,50,SHY) )
        self._addEnemy( enemy.BooFast(1050,122,SHY) )
        self._addEnemy( enemy.Boo(1100,324,SHY) )
        self._addEnemy( enemy.Boo(1181,234,SHY) )
        self._addEnemy( enemy.BooFast(1290,0,SHY) )
        self._addEnemy( enemy.BooFast(1321,150,SHY) )
        self._addEnemy( enemy.BooFast(1420,122,SHY) )
        self._addEnemy( enemy.Boo(1509,429,SHY) )
        self._addEnemy( enemy.Boo(1581,214,SHY) )
        self._addEnemy( enemy.BooFast(1690,300,SHY) )
            #player leaves here
        self._addTerrain( levelobject.MarioPipeDownTeleporter2(2300,450) )

            #checkpoint to stop level from ending
        self._addCheckpoint(10000)


"""
    Tutorial level
"""

class Level0(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 0
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl0.wav'

        #background
        self.background = None
        bg1  = 'images/levelsprites/tut/tutbg.gif'
        bg2  = 'images/levelsprites/tut/tutbg2.gif'
        self.parallax = Parallax(bg1,0,-400, bg2,0,100)

            #checkpoint
        self._addCheckpoint(10)
            #floor
        self._addTerrain( levelobject.TutGround(0, SCREEN_HEIGHT-16) )
            #signs
        self._addTerrain( levelobject.TutSign1(20, SCREEN_HEIGHT-254) )
        self._addTerrain( levelobject.TutSign2(350, SCREEN_HEIGHT-146) )
        self._addTerrain( levelobject.TutSign3(850, SCREEN_HEIGHT-148) )
        self._addTerrain( levelobject.TutSign4(1150, SCREEN_HEIGHT-153) )
            #enemies
        self._addNode( levelobject.Node(870,550) )
        self._addEnemy( enemy.Pup1(900,550,PLATFORM) )
        self._addEnemy( enemy.Kit1(1150,550,PLATFORM) )
        self._addNode( levelobject.Node(1200,550) )
            #floor
        self._addTerrain( levelobject.TutGround(1500, SCREEN_HEIGHT-16) )
            #more signs
        self._addTerrain( levelobject.TutSign5(1650, SCREEN_HEIGHT-148) )
            #enemies
        self._addNode( levelobject.Node(1700,550) )
        self._addEnemy( enemy.Pup2(1730,550,PLATFORM) )
        self._addEnemy( enemy.Kit2(1970,550,PLATFORM) )
        self._addNode( levelobject.Node(2000,550) )
        self._addEnemy( enemy.Kit1(2500,550,NONE) )
            #third floor
        self._addTerrain( levelobject.TutGround(2930, SCREEN_HEIGHT-16) )
        self._addTerrain( levelobject.TutSign6(3000, SCREEN_HEIGHT-161) )
            #lots of enemies
        self._addNode( levelobject.Node(3100, 550) )
        self._addEnemy( enemy.Pup3(3150,550,PLATFORM) )
        self._addEnemy( enemy.Pup2(3200,550,NONE) )
        self._addEnemy( enemy.Kit2(3300,550,PLATFORM) )
        self._addEnemy( enemy.Pup1(3400,550,NONE) )
        self._addEnemy( enemy.Pup1(3550,550,PLATFORM) )
        self._addEnemy( enemy.Kit1(3650,550,PLATFORM) )
        self._addEnemy( enemy.Kit1(3700,550,NONE) )
        self._addNode( levelobject.Node(3750, 550) )
            #end of level
        self._addCheckpoint(3900)


"""
    Mario level
"""

class Level1(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 1
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl1.wav'

        #background
        #self.background = levelobject.StaticImage('images/levelsprites/smw/smwbg1.png',0,-2400)
        self.background = None
        bg1  = 'images/levelsprites/smw/smwbg1.png'
        bg2  = 'images/levelsprites/smw/smwbg2.png'
        self.parallax = Parallax(bg1,0,-261, bg2,0,-2400)

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-16) )
        self._addCheckpoint(0)
            #goombas
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.Goomba(500,400, PLATFORM) )
        self._addEnemy( enemy.Goomba(700,400, FLOOR) )
        self._addEnemy( enemy.Goomba(800,400, PLATFORM) )
        self._addEnemy( enemy.Goomba(900,400, FLOOR) )
        self._addEnemy( enemy.Goomba(1100,400, PLATFORM) )
        self._addEnemy( enemy.Goomba(1300,400, FLOOR) )
        self._addNode( levelobject.Node(1500,550) )
            #ParaKoopa
        self._addNode( levelobject.Node(1700, 200) )
        self._addEnemy( enemy.ParaKoopa(1700,400, FLYVERT) )
        self._addNode( levelobject.Node(1700, 500) )
        self._addTerrain( levelobject.MarioPlatform6(1750,400) )
            #ParaKoopa
        self._addNode( levelobject.Node(2000, 0) )
        self._addEnemy( enemy.ParaKoopa(2000,300, FLYVERT) )
        self._addNode( levelobject.Node(2000, 400) )
        self._addTerrain( levelobject.MarioPlatform6(2050,200) )
            #empty platform
        self._addTerrain( levelobject.MarioPlatform6(2350,350) )
            #floor + nodes for fuzzies + checkpoint
        self._addNode( levelobject.Node(2600,SCREEN_HEIGHT-32,0,0,-1) )
        self._addNode( levelobject.Node(2600,SCREEN_HEIGHT-75,0,0,-1) )
        self._addNode( levelobject.Node(2600,SCREEN_HEIGHT-115,0,0,-1) )
        self._addNode( levelobject.Node(2600,SCREEN_HEIGHT-150,0,0,-1) )
        self._addTerrain( levelobject.MarioGround1632(2600,SCREEN_HEIGHT-16) )
        self._addTerrain( levelobject.Checkpoint(2700,SCREEN_HEIGHT-153) )
        self._addCheckpoint(2700)
        self._addNode( levelobject.Node(4200,SCREEN_HEIGHT-75,0,0,-1))
        self._addNode( levelobject.Node(4200,SCREEN_HEIGHT-32,0,0,-1) )
        self._addNode( levelobject.Node(4200,SCREEN_HEIGHT-75,0,0,-1) )
        self._addNode( levelobject.Node(4200,SCREEN_HEIGHT-115,0,0,-1) )
        self._addNode( levelobject.Node(4200,SCREEN_HEIGHT-150,0,0,-1) )
            #enemies + heart
        self._addEnemy( enemy.Fuzzy(2900, 500, HOP) )
        self._addEnemy( enemy.ParaKoopa(3100, 150, FLYSWOOP) )
        self._addHeart( levelobject.Heart(3275,300) )
        self._addEnemy( enemy.Fuzzy(3150, 500, HOP) )
        self._addTerrain( levelobject.MarioPlatform6(3200,400) )
        self._addEnemy( enemy.Fuzzy(3400, 500, HOP) )
        self._addEnemy( enemy.Fuzzy(3600, 500, HOP) )
        self._addEnemy( enemy.Fuzzy(3800, 500, HOP) )
        self._addEnemy( enemy.Fuzzy(4000, 500, HOP) )
            #mushroom platforms + ammo
        self._addTerrain( levelobject.MarioMushroomPlatform(4450,500) )
        self._addEnemy( enemy.Fuzzy(4470, 500, JUMP) )
        self._addTerrain( levelobject.MarioMushroomPlatform(4700,300) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(4716,400) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(4716,502) )
        self._addEnemy( enemy.Fuzzy(4720, 300, JUMP) )
        self._addAmmo( levelobject.Ammo(4720,250) )
        self._addTerrain( levelobject.MarioMushroomPlatform(5000,300) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(5016,400) )
        self._addTerrain( levelobject.MarioMushroomPlatformBase(5016,502) )
        self._addEnemy( enemy.Fuzzy(5050, 300, JUMP) )
            #teleporter to level -1
        self._addTerrain( levelobject.MarioPipeDownTeleporter1(5270,
            SCREEN_HEIGHT-120) )
            #movable platform + enemies on clouds
        self._addNode( levelobject.Node(5200,300,0,0,-1))
        self._addTerrain( levelobject.MarioMovablePlatform(5400,300, 5) )
        self._addTerrain( levelobject.MarioCloud(5600,200) )
        self._addEnemy( enemy.Fuzzy(5660, 100, JUMP) )
        self._addTerrain( levelobject.MarioCloud(6200,200) )
        self._addEnemy( enemy.Fuzzy(6260, 100, JUMP) )
        self._addNode( levelobject.Node(6700,300,0,0,-1))
            #teleport from level -1
        self._addTerrain( levelobject.MarioPipeDown(6450,
            SCREEN_HEIGHT-120) )
            #checkpoint
        self._addTerrain( levelobject.Checkpoint(6850,63) )
        self._addCheckpoint(6800)
            #platforms w shyguy
        self._addNode( levelobject.Node(6800,180) )
        self._addTerrain( levelobject.MarioPlatform12(6800,200) )
        self._addEnemy( enemy.ShyGuy(6970, 180, PLATFORM) )
        self._addNode( levelobject.Node(7174,180) )
            #vertical platform
        self._addNode( levelobject.Node(7300,180,0,0,0,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(7300,100,0,5) )
        self._addNode( levelobject.Node(7300,-500,0,0,0,-1) )
            #clouds + koopas
        self._addTerrain( levelobject.MarioCloud(7510, -500))
        self._addTerrain( levelobject.MarioCloud(7800, -200) )
        self._addNode( levelobject.Node(7830, -300) )
        self._addEnemy( enemy.ParaKoopa(7830,-600, FLYVERT) )
        self._addNode( levelobject.Node(7830, -600) )
        self._addTerrain( levelobject.MarioCloud(7870, -720) )
        self._addEnemy( enemy.ParaKoopa(7800,-959, FLYSWOOP) )
        self._addTerrain( levelobject.MarioCloud(8100, -400) )
            #surprise flying koopas for previous section
        self._addEnemy( enemy.ParaKoopa(8530,-2000, FLYATTACK) )
        self._addEnemy( enemy.ParaKoopa(8730,-2500, FLYATTACK) )
            #two koopas in between two clouds
        self._addTerrain( levelobject.MarioCloud(8400,-600) )
        self._addNode( levelobject.Node(8600, -500) )
        self._addEnemy( enemy.ParaKoopa(8600,-994, FLYVERT) )
        self._addNode( levelobject.Node(8600, -1000) )
        self._addNode( levelobject.Node(8750, -500) )
        self._addEnemy( enemy.ParaKoopa(8750,-583, FLYVERT) )
        self._addNode( levelobject.Node(8750, -1000) )
        self._addTerrain( levelobject.MarioCloud(8850,-600) )
            #two koopas in between two clouds
        self._addTerrain( levelobject.MarioCloud(9200,-700) )
        self._addNode( levelobject.Node(9400, -600) )
        self._addEnemy( enemy.ParaKoopa(9400,-1094, FLYVERT) )
        self._addNode( levelobject.Node(9400, -1100) )
        self._addNode( levelobject.Node(9550, -600) )
        self._addEnemy( enemy.ParaKoopa(9550,-683, FLYVERT) )
        self._addNode( levelobject.Node(9550, -1100) )
        self._addTerrain( levelobject.MarioCloud(9650,-700) )
        self._addTerrain( levelobject.Checkpoint(9700,-837) )
        self._addCheckpoint(9700)
            #moving platforms back to ground
        self._addNode( levelobject.Node(9850, -650,0,0,-1,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(9900,-600,5,5) )
        self._addNode( levelobject.Node(10250, -250,0,0,-1,-1) )

        self._addNode( levelobject.Node(10450,-500) )
        self._addEnemy( enemy.ParaKoopa(10450,-300, FLYVERT) )
        self._addNode( levelobject.Node(10450,-100) )

        self._addNode( levelobject.Node(10600,-400,0,0,0,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(10600,-200,0,5) )
        self._addNode( levelobject.Node(10600,100,0,0,0,-1) )

        self._addNode( levelobject.Node(10850,-700) )
        self._addEnemy( enemy.ParaKoopa(10850,-500, FLYVERT) )
        self._addNode( levelobject.Node(10850,-300) )
        self._addEnemy( enemy.ParaKoopa(10850,   0, FLYVERT) )
        self._addNode( levelobject.Node(10850, 100) )
        self._addHeart( levelobject.Heart(11000,-500) )
        self._addNode( levelobject.Node(11000,-100,0,0,0,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(11000,0,0,5) )
        self._addNode( levelobject.Node(11000,400,0,0,0,-1) )
            #floor, checkpoint, shyguys for distractions, and attacking parakoopas
        self._addTerrain( levelobject.Checkpoint(11350,SCREEN_HEIGHT-153) )
        self._addCheckpoint(11300)
        self._addTerrain( levelobject.MarioGround1632(11300,SCREEN_HEIGHT-16) )
        self._addAmmo( levelobject.Ammo(11500,450) )
        self._addAmmo( levelobject.Ammo(11800,450) )
        self._addEnemy( enemy.ShyGuy(11800,450, FLOOR) )
        self._addEnemy( enemy.ShyGuy(12000,450, FLOOR) )
        self._addEnemy( enemy.ShootingShyGuy(12500,400, RPROJ, self) )
        self._addEnemy( enemy.ParaKoopa(12400, -100, FLYATTACK) )
        self._addEnemy( enemy.ParaKoopa(12600, 300, FLYATTACK) )

            #platforms with projectile enemies
        self._addTerrain( levelobject.MarioPlatform6(13000,400) )
        self._addEnemy( enemy.ShootingShyGuy(13100,200, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(13200,200) )
        self._addEnemy( enemy.ShootingShyGuy(13300,100, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(13400,0) )
        self._addEnemy( enemy.ShootingShyGuy(13500,-100, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(13600,-200) )
        self._addEnemy( enemy.ShootingShyGuy(13700,-300, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(13800, 0) )
        self._addEnemy( enemy.ShootingShyGuy(13900,-100, RPROJSTAND, self) )
        self._addTerrain( levelobject.MarioPlatform6(13800,-400) )
        self._addEnemy( enemy.ShootingShyGuy(13900,-500, RPROJSTAND, self) )
        self._addTerrain( levelobject.MarioPlatform6(13800, -600) )
        self._addEnemy( enemy.ShootingShyGuy(13900,-700, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(14200, 0) )
        self._addEnemy( enemy.ShootingShyGuy(14300,-100, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(14400,200) )
        self._addEnemy( enemy.ShootingShyGuy(14500,100, RPROJSTAND, self) )

        self._addTerrain( levelobject.MarioPlatform6(14600,400) )
        self._addEnemy( enemy.ShootingShyGuy(14700,200, RPROJSTAND, self) )

            #end of level
        self._addTerrain( levelobject.MarioGround1632(15000,SCREEN_HEIGHT-16) )
        self._addEnemy( enemy.Mario(15700,400, FLOOR) )
        self._addEnemy( enemy.Luigi(15800,400, FLOOR) )
        self._addTerrain( levelobject.MarioCastle(15700,SCREEN_HEIGHT-338) )
        self._addCheckpoint(15700)


"""
    Sonic level
"""

class Level2(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 2
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl2.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/sonic/background2.png',0,-250)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.SonicPlatformThick4(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)
        
        self._addTerrain( levelobject.SonicPlatformThick4(589,SCREEN_HEIGHT-64) )
        #spam some annoying enemies
        self._addNode( levelobject.Node(589,SCREEN_HEIGHT-80))
        self._addEnemy( enemy.Chao(700,400, PLATFORM))
        self._addEnemy( enemy.Chao(750,400, PLATFORM))
        self._addEnemy( enemy.Chao(800,400, PLATFORM))
        self._addEnemy( enemy.Chao(850,400, PLATFORM))
        self._addEnemy( enemy.Chao(900,400, PLATFORM))
        self._addEnemy( enemy.Chao(950,400, PLATFORM))
        self._addEnemy( enemy.Chao(1000,400, PLATFORM))
        self._addEnemy( enemy.Chao(1050,400, PLATFORM))
        self._addEnemy( enemy.Chao(1100,400, PLATFORM))
        self._addNode( levelobject.Node(1150,SCREEN_HEIGHT-80))
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*2,SCREEN_HEIGHT-128) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*3,SCREEN_HEIGHT-64) )
        #spam some more enemies
        self._addNode( levelobject.Node(589*3,SCREEN_HEIGHT-80))
        self._addEnemy( enemy.Chao(1800,400, PLATFORM))
        self._addEnemy( enemy.Chao(1850,400, PLATFORM))
        self._addEnemy( enemy.Chao(1900,400, PLATFORM))
        self._addEnemy( enemy.Chao(1950,400, PLATFORM))
        self._addEnemy( enemy.Chao(2000,400, PLATFORM))
        self._addEnemy( enemy.Chao(2050,400, PLATFORM))
        self._addEnemy( enemy.Chao(2100,400, PLATFORM))
        self._addEnemy( enemy.Chao(2150,400, PLATFORM))
        self._addEnemy( enemy.Chao(2200,400, PLATFORM))
        self._addNode( levelobject.Node(589*4-16,SCREEN_HEIGHT-80))
        
        #jumping enemies
        self._addNode( levelobject.Node(2356,SCREEN_HEIGHT-48,0,0,-1) )
        self._addNode( levelobject.Node(2356,SCREEN_HEIGHT-91,0,0,-1) )
        self._addNode( levelobject.Node(2356,SCREEN_HEIGHT-131,0,0,-1) )
        self._addNode( levelobject.Node(2356,SCREEN_HEIGHT-166,0,0,-1) )
        self._addNode( levelobject.Node(2356,SCREEN_HEIGHT-180,0,0,-1) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*4,SCREEN_HEIGHT-48) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*5,SCREEN_HEIGHT-32) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*6,SCREEN_HEIGHT-48) )
        #Jumping bunnies (she's some minor character, isn't she?)
        self._addEnemy( enemy.Cream(2450,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(2750,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(2950,SCREEN_HEIGHT-60, HOP) )
        self._addHeart( levelobject.Heart(3000,300) )
        self._addEnemy( enemy.Cream(3150,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(3250,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(3350,SCREEN_HEIGHT-60, HOP) )
        self._addNode( levelobject.Node(3534,SCREEN_HEIGHT-48,0,0,-1) )
        self._addNode( levelobject.Node(3534,SCREEN_HEIGHT-91,0,0,-1) )
        self._addNode( levelobject.Node(3534,SCREEN_HEIGHT-131,0,0,-1) )
        self._addNode( levelobject.Node(3534,SCREEN_HEIGHT-166,0,0,-1) )
        self._addNode( levelobject.Node(3534,SCREEN_HEIGHT-180,0,0,-1) )
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*7,SCREEN_HEIGHT-64) )
        #make a nice gap here
        self._addTerrain( levelobject.SonicPlatformThick4(589*9-589/2,SCREEN_HEIGHT-64) )
        self._addNode( levelobject.Node(5000, SCREEN_HEIGHT-264) )
        self._addEnemy( enemy.Robotnik(5000,SCREEN_HEIGHT-200, FLYVERT) )
        self._addNode( levelobject.Node(5000, SCREEN_HEIGHT-100) )
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*10,SCREEN_HEIGHT-128) )
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*11,SCREEN_HEIGHT-160) )
        self._addTerrain( levelobject.SonicCheckers(589*11,SCREEN_HEIGHT-28))
        self._addEnemy( enemy.Gamma(6500,450, FLOOR) )
        self._addEnemy( enemy.Gamma(6500,450, FLOOR) )
        
        self._addTerrain( levelobject.SonicPlatformThin(589*12+589/2,SCREEN_HEIGHT-212) )

        self._addNode( levelobject.Node(7805,SCREEN_HEIGHT-264,0,0,-1) )
        self._addNode( levelobject.Node(7805,SCREEN_HEIGHT-294,0,0,-1) )
        self._addNode( levelobject.Node(7805,SCREEN_HEIGHT-324,0,0,-1) )
        self._addNode( levelobject.Node(7805,SCREEN_HEIGHT-354,0,0,-1) )
        self._addNode( levelobject.Node(7805,SCREEN_HEIGHT-384,0,0,-1) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*13+589/4,SCREEN_HEIGHT-256) )
        self._addTerrain( levelobject.SonicCheckers(589*13+589/4,SCREEN_HEIGHT-256+132))
        self._addEnemy( enemy.Cream(7900,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(8000,SCREEN_HEIGHT-60, HOP) )
        self._addEnemy( enemy.Cream(8100,SCREEN_HEIGHT-60, HOP) )
        self._addNode( levelobject.Node(8393,SCREEN_HEIGHT-264,0,0,-1) )
        self._addNode( levelobject.Node(8393,SCREEN_HEIGHT-294,0,0,-1) )
        self._addNode( levelobject.Node(8393,SCREEN_HEIGHT-324,0,0,-1) )
        self._addNode( levelobject.Node(8393,SCREEN_HEIGHT-354,0,0,-1) )
        self._addNode( levelobject.Node(8393,SCREEN_HEIGHT-384,0,0,-1) )
        
        self._addNode( levelobject.Node(8500, SCREEN_HEIGHT-500) )
        self._addEnemy( enemy.Robotnik(8500,SCREEN_HEIGHT-400, FLYVERT) )
        self._addNode( levelobject.Node(8500, SCREEN_HEIGHT-200) )
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*15,SCREEN_HEIGHT-212) )
        self._addTerrain( levelobject.SonicCheckers(589*15,SCREEN_HEIGHT-212+132))
        self._addTerrain( levelobject.Checkpoint(9000,SCREEN_HEIGHT-212-137) )
        self._addCheckpoint(9000)
        
        self._addNode( levelobject.Node(589*16,SCREEN_HEIGHT-64) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*16,SCREEN_HEIGHT-32) )
        self._addEnemy( enemy.Chao(589*16+50,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+100,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+150,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+200,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+250,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+300,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+350,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+400,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*16+450,400, PLATFORM))
        self._addNode( levelobject.Node(589*17-32,SCREEN_HEIGHT-64) )
        self._addNode( levelobject.Node(589*17,SCREEN_HEIGHT-96) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*17,SCREEN_HEIGHT-64) )
        self._addEnemy( enemy.Chao(589*17+50,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+100,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+150,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+200,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+250,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+300,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+350,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+400,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*17+450,400, PLATFORM))
        self._addEnemy( enemy.Cream(589*17+280,400, HOP) )
        self._addNode( levelobject.Node(589*18-32,SCREEN_HEIGHT-96) )
        self._addNode( levelobject.Node(589*18,SCREEN_HEIGHT-128) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*18,SCREEN_HEIGHT-96) )
        self._addEnemy( enemy.Chao(589*18+50,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+100,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+150,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+200,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+250,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+300,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+350,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+400,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*18+450,400, PLATFORM))
        self._addEnemy( enemy.Cream(589*18+280,400, HOP) )
        self._addEnemy( enemy.Cream(589*18+310,400, HOP) )
        self._addNode( levelobject.Node(589*19-32,SCREEN_HEIGHT-128) )
        self._addNode( levelobject.Node(589*19,SCREEN_HEIGHT-160) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*19,SCREEN_HEIGHT-128) )
        self._addEnemy( enemy.Chao(589*19+50,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+100,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+150,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+200,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+250,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+300,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+350,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+400,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*19+450,400, PLATFORM))
        self._addEnemy( enemy.Cream(589*19+280,400, HOP) )
        self._addEnemy( enemy.Cream(589*19+310,400, HOP) )
        self._addEnemy( enemy.Cream(589*19+340,400, HOP) )
        self._addNode( levelobject.Node(589*20-32,SCREEN_HEIGHT-160) )
        self._addNode( levelobject.Node(589*20,SCREEN_HEIGHT-196) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*20,SCREEN_HEIGHT-160) )
        self._addTerrain( levelobject.SonicCheckers(589*15,SCREEN_HEIGHT-160+132))
        self._addEnemy( enemy.Chao(589*20+50,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+100,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+150,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+200,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+250,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+300,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+350,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+400,400, PLATFORM))
        self._addEnemy( enemy.Chao(589*20+450,400, PLATFORM))
        self._addNode( levelobject.Node(589*21-32,SCREEN_HEIGHT-196) )
        self._addNode( levelobject.Node(589*21,SCREEN_HEIGHT-228) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*21,SCREEN_HEIGHT-196) )
        self._addTerrain( levelobject.SonicCheckers(589*15,SCREEN_HEIGHT-196+132))
        self._addNode( levelobject.Node(589*22-32,SCREEN_HEIGHT-228) )
        
        self._addTerrain( levelobject.SonicPlatformThin(589*23-200,SCREEN_HEIGHT-290) )
        self._addTerrain( levelobject.Checkpoint(589*23-200,SCREEN_HEIGHT-290-137) )
        self._addCheckpoint(589*23-200)
        
        self._addTerrain( levelobject.SonicPlatformThick4(589*23,SCREEN_HEIGHT-32) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*24,SCREEN_HEIGHT-28) )
        self._addTerrain( levelobject.SonicPlatformThick4(589*25,SCREEN_HEIGHT-32) )
        
        
        #bosses
        self._addNode( levelobject.Node(13600,550) )
        self._addNode( levelobject.Node(13600,530) )
        self._addNode( levelobject.Node(13600,510) )
        self._addNode( levelobject.Node(13600,490) )
        self._addNode( levelobject.Node(13600,470) )
        self._addNode( levelobject.Node(13600,450) )
        self._addNode( levelobject.Node(13600,430) )
        self._addNode( levelobject.Node(13600,410) )
        self._addEnemy( enemy.Sonic(14000,500, PLATFORM) )
        self._addEnemy( enemy.Sonic(14200,500, PLATFORM) )
        self._addEnemy( enemy.Robotnik(13700,350, FLYSWOOP))
        self._addEnemy( enemy.Sonic(14400,500, PLATFORM) )
        self._addNode( levelobject.Node(14500,550) )
        self._addNode( levelobject.Node(14500,530) )
        self._addNode( levelobject.Node(14500,510) )
        self._addNode( levelobject.Node(14500,490) )
        self._addNode( levelobject.Node(14500,470) )
        self._addNode( levelobject.Node(14500,450) )
        self._addNode( levelobject.Node(14500,430) )
        self._addNode( levelobject.Node(14500,410) )
        
        self._addCheckpoint(14500)

"""
    Megaman level
"""

class Level3(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 3
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init enemies stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl3.wav'

        #background
        #self.background = levelobject.StaticImage('images/levelsprites/megaman/background.png',0,-55)
        self.background = None
        bg1  = 'images/levelsprites/megaman/background.png'
        bg2  = 'images/levelsprites/megaman/backgroundTrans.png'
        self.parallax = Parallax(bg1,0,-55,bg2,0,0)

        #Ammo and Heart Examples
        #self._addAmmo3( levelobject.Ammo3( 552, SCREEN_HEIGHT-506 ) )
        #self._addHeart3( levelobject.Heart3( 422, SCREEN_HEIGHT-406 ) )
        #self._addHeart( levelobject.Heart( 422, SCREEN_HEIGHT-206 ) )
        #self._addAmmo( levelobject.Ammo( 552, SCREEN_HEIGHT-206 ) )

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MegamanPlatThin3(0,SCREEN_HEIGHT-14) )
        self._addCheckpoint(0)
        self._addTerrain( levelobject.MegamanPlatNorm(384,SCREEN_HEIGHT-65) )
        self._addHeart( levelobject.Heart( 422, SCREEN_HEIGHT-206 ) )
        #self._addHeart3( levelobject.Heart3( 422, SCREEN_HEIGHT-406 ) )
        self._addTerrain( levelobject.MegamanPlatTallerWide(497,SCREEN_HEIGHT-96) )
        self._addAmmo( levelobject.Ammo( 552, SCREEN_HEIGHT-206 ) )
        #self._addAmmo3( levelobject.Ammo3( 552, SCREEN_HEIGHT-506 ) )
        
        self._addNode( levelobject.Node(794,SCREEN_HEIGHT-170) )
        self._addEnemy( enemy.BoyRobot1(900,SCREEN_HEIGHT-220, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin2(789,SCREEN_HEIGHT-150) )
        self._addNode( levelobject.Node(1035,SCREEN_HEIGHT-170) )
        
        self._addTerrain( levelobject.MegamanPlatTallerWide(1145,SCREEN_HEIGHT-96) )
        self._addAmmo( levelobject.Ammo( 1200, SCREEN_HEIGHT-206 ) )
        self._addNode( levelobject.Node(1335,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot1(1400,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(1595,SCREEN_HEIGHT-85) )
        self._addTerrain( levelobject.MegamanPlatLong(1337,SCREEN_HEIGHT-65) )
        self._addNode( levelobject.Node(1700,SCREEN_HEIGHT-250) )
        self._addEnemy( enemy.Drone(1700,SCREEN_HEIGHT-200, FLYVERT) )
        self._addNode( levelobject.Node(1700,SCREEN_HEIGHT-70) )
        self._addNode( levelobject.Node(1800,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot1(1900,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot1(2000,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(2130,SCREEN_HEIGHT-85) ) 
        self._addEnemy( enemy.BoyRobot1(2200,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot2(2400,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot1(2700,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(2900,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot1(2950,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(3190,SCREEN_HEIGHT-85) )
        self._addTerrain( levelobject.MegamanPlatTallerWide(3193,SCREEN_HEIGHT-96) )
        #self._addStar( levelobject.Star( 3275, SCREEN_HEIGHT-450 ) )
        self._addNode( levelobject.Node(3383,SCREEN_HEIGHT-148) )
        self._addEnemy( enemy.BoyRobot2(3400,SCREEN_HEIGHT-168, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatTallestWide(3385,SCREEN_HEIGHT-128) )
        self._addNode( levelobject.Node(3575,SCREEN_HEIGHT-148) )
        
        self._addTerrain( levelobject.MegamanPlatTallestWide(3727,SCREEN_HEIGHT-128) )
        self._addNode( levelobject.Node(3917,SCREEN_HEIGHT-116) )
        self._addEnemy( enemy.BoyRobot1(4000,SCREEN_HEIGHT-135, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatTallerWide(3919,SCREEN_HEIGHT-96) )
        self._addNode( levelobject.Node(4109,SCREEN_HEIGHT-116) )
        
        self._addNode( levelobject.Node(4283,SCREEN_HEIGHT-116) )
        self._addEnemy( enemy.BoyRobot2(4300,SCREEN_HEIGHT-135, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatTallerWide(4286,SCREEN_HEIGHT-96) )
        self._addNode( levelobject.Node(4470,SCREEN_HEIGHT-116) )
        self._addTerrain( levelobject.MegamanPlatTallestWide(4475,SCREEN_HEIGHT-128) )
        self._addCheckpoint(4860)
        
        self._addNode( levelobject.Node(4850,SCREEN_HEIGHT-170) )
        self._addEnemy( enemy.BoyRobot2(5000,SCREEN_HEIGHT-190, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(4853,SCREEN_HEIGHT-150) )
        self._addNode( levelobject.Node(5230,SCREEN_HEIGHT-170) )
        
        self._addNode( levelobject.Node(5402,SCREEN_HEIGHT-300) )
        self._addEnemy( enemy.BoyRobot2(5500,SCREEN_HEIGHT-320, PLATFORM) )
        self._addEnemy( enemy.BoyRobot3(5660,SCREEN_HEIGHT-320, PLATFORM) )
        self._addHeart( levelobject.Heart( 5585, SCREEN_HEIGHT-470 ) )
        self._addTerrain( levelobject.MegamanPlatThin3(5412,SCREEN_HEIGHT-280) )
        self._addNode( levelobject.Node(5790,SCREEN_HEIGHT-300) )
        self._addTerrain( levelobject.MegamanPlatThin3(5412,SCREEN_HEIGHT-34) )
        
        self._addNode( levelobject.Node(5968,SCREEN_HEIGHT-170) )
        self._addEnemy( enemy.BoyRobot2(6200,SCREEN_HEIGHT-190, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(5971,SCREEN_HEIGHT-150) )
        self._addNode( levelobject.Node(6352,SCREEN_HEIGHT-170) )
        
        self._addNode( levelobject.Node(6520,SCREEN_HEIGHT-300) )
        self._addEnemy( enemy.BoyRobot1(6600,SCREEN_HEIGHT-320, PLATFORM) )
        self._addEnemy( enemy.BoyRobot2(6825,SCREEN_HEIGHT-320, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(6530,SCREEN_HEIGHT-280) )
        self._addNode( levelobject.Node(6909,SCREEN_HEIGHT-300) )
        self._addAmmo( levelobject.Ammo( 6617, SCREEN_HEIGHT-110 ) )
        self._addAmmo( levelobject.Ammo( 6745, SCREEN_HEIGHT-110 ) )
        self._addTerrain( levelobject.MegamanPlatThin3(6530,SCREEN_HEIGHT-34) )
        
        self._addNode( levelobject.Node(7085,SCREEN_HEIGHT-150) )
        self._addEnemy( enemy.BoyRobot2(7200,SCREEN_HEIGHT-190, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(7089,SCREEN_HEIGHT-130) )
        self._addNode( levelobject.Node(7469,SCREEN_HEIGHT-150) )
        
        self._addNode( levelobject.Node(7644,SCREEN_HEIGHT-54) )
        self._addEnemy( enemy.BoyRobot3(7700,SCREEN_HEIGHT-74, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(7648,SCREEN_HEIGHT-34) )
        self._addNode( levelobject.Node(8028,SCREEN_HEIGHT-54) )
        
        #Do you feel it yet? I don't know man, the platforms are moving...
        
        self._addNode( levelobject.Node500(8190,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(8200,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot2(8400,SCREEN_HEIGHT-520, PLATFORM) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 8207, SCREEN_HEIGHT-150, 0, 3 ) )
        self._addNode( levelobject.Node(8200,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(8595,SCREEN_HEIGHT-505) )
        
        self._addAmmo( levelobject.Ammo( 8631, SCREEN_HEIGHT-700 ) )
        
        self._addNode( levelobject.Node500(8749,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(8755,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot1(9000,SCREEN_HEIGHT-520, PLATFORM) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 8766, SCREEN_HEIGHT-450, 0, 3 ) )
        self._addNode( levelobject.Node(8755,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(9155,SCREEN_HEIGHT-505) )
        
        self._addAmmo3( levelobject.Ammo3(9189, SCREEN_HEIGHT-700 ) )
        
        self._addNode( levelobject.Node500(9308,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(9315,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot3(9600,SCREEN_HEIGHT-520, PLATFORM) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 9325, SCREEN_HEIGHT-250, 0, 3 ) )
        self._addNode( levelobject.Node(9315,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(9714,SCREEN_HEIGHT-505) )
        
        self._addHeart( levelobject.Heart( 9772, SCREEN_HEIGHT-700 ) )
        
        self._addNode( levelobject.Node500(9867,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(9874,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot2(10100,SCREEN_HEIGHT-520, PLATFORM) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 9884, SCREEN_HEIGHT-50, 0, 3 ) )
        self._addNode( levelobject.Node(9874,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(10273,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(10345,SCREEN_HEIGHT-520) )
        self._addEnemy( enemy.Drone(10345,SCREEN_HEIGHT-500, FLYVERT) )
        self._addNode( levelobject.Node(10345,SCREEN_HEIGHT-250) )
        
        self._addNode( levelobject.Node500(10426,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(10433,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot3(10650,SCREEN_HEIGHT-520, RPROJSTAND, self) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 10443, SCREEN_HEIGHT-350, 0, 3 ) )
        self._addNode( levelobject.Node(10433,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(10832,SCREEN_HEIGHT-505) )

        self._addNode( levelobject.Node(10900,SCREEN_HEIGHT-350) )
        self._addEnemy( enemy.Drone(10900,SCREEN_HEIGHT-200, FLYVERT) )
        self._addNode( levelobject.Node(10900,SCREEN_HEIGHT-70) )

        self._addNode( levelobject.Node500(10985,SCREEN_HEIGHT-505) )
        
        self._addNode( levelobject.Node(10990,SCREEN_HEIGHT-14,0,0,-1,-1) )
        self._addEnemy( enemy.BoyRobot3(11250,SCREEN_HEIGHT-290, RPROJSTAND, self) )
        self._addTerrain( levelobject.MegamanMovablePlat3( 11002, SCREEN_HEIGHT-250, 0, 3 ) )
        self._addNode( levelobject.Node(10990,SCREEN_HEIGHT-500,0,0,-1,-1) )
        
        self._addNode( levelobject.Node500(11391,SCREEN_HEIGHT-505) )
        
        self._addCheckpoint(11570)
        self._addNode( levelobject.Node(11563,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot2(11600,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot1(11700,SCREEN_HEIGHT-105, RPROJ, self) )
        self._addEnemy( enemy.BoyRobot2(11800,SCREEN_HEIGHT-105, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatLong(11563,SCREEN_HEIGHT-65) )
        self._addNode( levelobject.Node(12485,SCREEN_HEIGHT-85) )
        self._addTerrain( levelobject.MegamanPlatThin2(12500,SCREEN_HEIGHT-220) )
        self._addHeart( levelobject.Heart( 12548, SCREEN_HEIGHT-267 ) )
        self._addHeart3( levelobject.Heart3( 12653, SCREEN_HEIGHT-267 ) )
        self._addNode( levelobject.Node(12850,SCREEN_HEIGHT-350) )
        self._addEnemy( enemy.Drone(12850,SCREEN_HEIGHT-200, FLYVERT) )
        self._addNode( levelobject.Node(12850,SCREEN_HEIGHT-70) )
        self._addTerrain( levelobject.MegamanPlatThin2(12956,SCREEN_HEIGHT-220) )
        self._addAmmo( levelobject.Ammo( 13000, SCREEN_HEIGHT-255 ) )
        self._addAmmo( levelobject.Ammo( 13085, SCREEN_HEIGHT-255 ) )
        self._addNode( levelobject.Node(13310,SCREEN_HEIGHT-250) )
        self._addEnemy( enemy.Drone(13310,SCREEN_HEIGHT-200, FLYVERT) )
        self._addNode( levelobject.Node(13310,SCREEN_HEIGHT-70) )
        
        self._addNode( levelobject.Node(13567,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot2(13700,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(14185,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot2(14600,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot3(14800,SCREEN_HEIGHT-105, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatLong(13567,SCREEN_HEIGHT-65) )
        self._addNode( levelobject.Node(14803,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot2(15000,SCREEN_HEIGHT-105, RPROJ, self) )
        self._addNode( levelobject.Node(15420,SCREEN_HEIGHT-85) )
        self._addNode( levelobject.Node(13985,SCREEN_HEIGHT-240) )
        self._addEnemy( enemy.BoyRobot2(14200,SCREEN_HEIGHT-260, PLATFORM) )
        self._addTerrain( levelobject.MegamanPlatThin3(14000,SCREEN_HEIGHT-220) )
        self._addNode( levelobject.Node(14380,SCREEN_HEIGHT-240) )
        self._addEnemy( enemy.BoyRobot3(14200,SCREEN_HEIGHT-320, RPROJ, self) )
        self._addNode( levelobject.Node(15418,SCREEN_HEIGHT-116) )
        self._addEnemy( enemy.BoyRobot3(15500,SCREEN_HEIGHT-126, RPROJ, self) )
        self._addTerrain( levelobject.MegamanPlatTallestWide(15423,SCREEN_HEIGHT-96) )
        self._addNode( levelobject.Node(15610,SCREEN_HEIGHT-116) )
        
        self._addNode( levelobject.Node(15790,SCREEN_HEIGHT-85) )
        self._addEnemy( enemy.BoyRobot2(15900,SCREEN_HEIGHT-105, PLATFORM) )
        self._addEnemy( enemy.BoyRobot3(16500,SCREEN_HEIGHT-105, RPROJ, self) )
        self._addEnemy( enemy.BoyRobot2(16100,SCREEN_HEIGHT-105, PLATFORM) )
        self._addNode( levelobject.Node(16790,SCREEN_HEIGHT-85) )
        self._addTerrain( levelobject.MegamanPlatLong(15790,SCREEN_HEIGHT-65) )
        self._addTerrain( levelobject.MegamanPlatLong(17646,SCREEN_HEIGHT-65) )
        self._addTerrain( levelobject.Serenity(17500,SCREEN_HEIGHT-665))
        self._addCheckpoint(17500)
        
#        #Megamans
#        self._addNode( levelobject.Node(20,550) )
#        self._addEnemy( enemy.BoyRobot1(700,400, PLATFORM) )
#        self._addEnemy( enemy.BoyRobot1(900,400, PLATFORM) )
#        self._addEnemy( enemy.BoyRobot1(1200,400, PLATFORM) )
#        self._addNode( levelobject.Node(1500,550) )


"""
    Metroid level
"""

class Level4(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 4
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init enemies stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl4.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/metroid/background.jpg',0,-55)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MetroidGround(0,SCREEN_HEIGHT-16) )
        self._addCheckpoint(0)
        
        #Space Pirates
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.SpacePirate(700,400, PLATFORM) )
        self._addEnemy( enemy.SpacePirate(800,400, PLATFORM) )
        self._addEnemy( enemy.SpacePirate(900,400, PLATFORM) )
        self._addNode( levelobject.Node(1000,550) )

        self._addHeart( levelobject.Heart(1200,550) )

        self._addNode( levelobject.Node(900,380) )
        self._addTerrain( levelobject.MetroidPlatform(900,400) )
        self._addEnemy( enemy.Metroid(950,350, PLATFORM) )
        self._addNode( levelobject.Node(900+256,380) )

        self._addNode( levelobject.Node(1300,230) )
        self._addTerrain( levelobject.MetroidPlatform(1300,250) )
        self._addEnemy( enemy.Metroid(1350,200, PLATFORM) )
        self._addEnemy( enemy.Metroid(1450,200, PLATFORM) )
        self._addNode( levelobject.Node(1300+256,230) )

        self._addNode( levelobject.Node(1700,80) )
        self._addTerrain( levelobject.MetroidPlatform(1700,100) )
        self._addEnemy( enemy.Metroid(1750,50, PLATFORM) )
        self._addEnemy( enemy.Metroid(1800,50, PLATFORM) )
        self._addEnemy( enemy.Metroid(1850,50, PLATFORM) )
        self._addNode( levelobject.Node(1700+256,80) )

        self._addTerrain( levelobject.MetroidPlatform(2100,-50) )
        self._addAmmo( levelobject.Ammo( 2100, -80 ) )
        self._addAmmo( levelobject.Ammo( 2150, -80 ) )
        self._addStar( levelobject.Star( 2200, -300 ) )
        self._addAmmo( levelobject.Ammo( 2250, -80 ) )
        self._addAmmo( levelobject.Ammo( 2300, -80 ) )
        
        self._addHeart( levelobject.Heart( 2150, -110 ) )
        self._addAmmo( levelobject.Ammo( 2200, -110 ) )
        self._addHeart( levelobject.Heart( 2300, -110 ) )

        self._addHeart( levelobject.Heart( 2230, -140 ) )

        #First level pyramid
        self._addNode( levelobject.Node(2300,530) )
        self._addTerrain( levelobject.MetroidPlatform(2300, 550) )
        self._addEnemy( enemy.SpacePirate(2350,500, PLATFORM) )
        self._addNode( levelobject.Node(2300+256,530) )

        self._addNode( levelobject.Node(2800,530) )
        self._addTerrain( levelobject.MetroidPlatform(2800, 550) )
        self._addEnemy( enemy.SpacePirate(2850,500, PLATFORM) )
        self._addNode( levelobject.Node(2800+256,530) )

        self._addNode( levelobject.Node(3300,530) )
        self._addTerrain( levelobject.MetroidPlatform(3300, 550) )
        self._addEnemy( enemy.SpacePirate(3350,500, PLATFORM) )
        self._addNode( levelobject.Node(3300+256,530) )

        self._addNode( levelobject.Node(3800,530) )
        self._addTerrain( levelobject.MetroidPlatform(3800, 550) )
        self._addEnemy( enemy.SpacePirate(3850,500, PLATFORM) )
        self._addNode( levelobject.Node(3800+256,530) )


        #Second level pyramid
        self._addNode( levelobject.Node(3050,330) )
        self._addTerrain( levelobject.MetroidPlatform(3050, 350) )
        self._addEnemy( enemy.SpacePirate(3100,300, PLATFORM) )
        self._addNode( levelobject.Node(3050+256,330) )

        self._addNode( levelobject.Node(3550,330) )
        self._addTerrain( levelobject.MetroidPlatform(3550, 350) )
        self._addEnemy( enemy.SpacePirate(3600,300, PLATFORM) )
        self._addNode( levelobject.Node(3550+256,330) )

        #Top of pyramid
        self._addTerrain( levelobject.MetroidPlatform(3300, 150) )

        #Ammo cache off to the right of the pyramid
        self._addNode( levelobject.Node(4500,530) )
        self._addTerrain( levelobject.MetroidPlatform(4500, 550) )
        self._addAmmo( levelobject.Ammo( 4550, 530 ) )
        self._addAmmo( levelobject.Ammo( 4550+50, 530 ) )
        self._addAmmo( levelobject.Ammo( 4550+100, 530 ) )
        self._addNode( levelobject.Node(4500+256,530) )

        #Going up
        self._addNode( levelobject.Node(3700,200,0,0,-1,-1) )
        self._addTerrain( levelobject.MetroidMovablePlatform( 3600, 150, 0, 5 ) )
        self._addNode( levelobject.Node(3700,-500,0,0,-1,-1) )

        
        #Death line
        self._addNode( levelobject.Node(3000,-600,0,0,-1,-1))
        self._addEnemy( enemy.FastMetroid(3100,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3200,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3300,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3400,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3500,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3600,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3700,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3800,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(3900,-600, FLYHORIZ) )
        self._addEnemy( enemy.FastMetroid(4000,-600, FLYHORIZ) )
        self._addNode( levelobject.Node(5000,-600,0,0,-1,-1))

        #Going right
        self._addNode( levelobject.Node(4000,-510,0,0,-1,-1) )
        self._addTerrain( levelobject.MetroidMovablePlatform( 4400, -510, 12, 0 ) )
        self._addNode( levelobject.Node(5780,-510,0,0,-1,-1) )

        #Next area
        self._addCheckpoint(6100)
        self._addTerrain( levelobject.MetroidGround(6000,-500) )

        self._addEnemy( enemy.Ridley(7000, -900, CUSTOM))

        self._addCheckpoint(7800)


"""
    Castlevania level
"""

class Level5(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 5
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init enemies stuff
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl5.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/castlevania/background.jpg',0,-2155)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addCheckpoint(0)

        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-32) )
        self._addTerrain( levelobject.MetroidPlatform(1230,-50) )
        self._addTerrain( levelobject.MetroidPlatform(600,-650) )

        self._addNode( levelobject.Node(2520,-660) )
        self._addTerrain( levelobject.MetroidPlatform(2500,-650) )
        self._addEnemy( enemy.Ghoul(2650,-700, PLATFORM) )
        self._addAmmo( levelobject.Ammo(2650, -680) )
        self._addHeart( levelobject.Heart( 2600, -680 ) )
        self._addAmmo( levelobject.Ammo(2550, -680) )
        self._addEnemy( enemy.GhoulSlow(2550,-700, PLATFORM) )
        self._addNode( levelobject.Node(2700,-660) )
        

        self._addTerrain( levelobject.MetroidPlatform(3000,-300) )
        self._addCheckpoint(3001)
        self._addTerrain( levelobject.Checkpoint(3000,-440) )


        #debug
        #self._addHeart( levelobject.Heart( 50, 500 ) )
        #self._addStar( levelobject.Star( 50, 500) )
        #self._addStar( levelobject.Star( 1500, 500) )
        
        #Ghouls
        self._addNode( levelobject.Node(80,550) )

        #fuck campers
        self._addEnemy( enemy.Ghoul(700,-2000, PLATFORM) )

        self._addEnemy( enemy.Ghoul(700,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(900,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(1000,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(1200,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(1250,450, PLATFORM) )

        #force player up
        self._addNode( levelobject.Node(2500,550) )
        self._addTerrain( levelobject.MarioGround1632(2500,SCREEN_HEIGHT-32) )
        self._addEnemy( enemy.Ghoul(2550,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2650,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2950,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3650,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3750,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2501,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2600,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2700,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2800,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(2900,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3000,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3100,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3200,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3300,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3400,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3500,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3600,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3700,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3800,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3900,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(4000,450, PLATFORM) )
        self._addEnemy( enemy.Ghoul(4100,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3250,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(3750,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(4050,450, PLATFORM) )
        self._addNode( levelobject.Node(4132,550) )


        self._addNode( levelobject.Node(1500,550) )
        self._addTerrain( levelobject.MarioGround1632(5100,SCREEN_HEIGHT-32) )

        self._addNode( levelobject.Node(5250,SCREEN_HEIGHT-50) )     
        self._addEnemy( enemy.GhoulSlow(5260,500, PLATFORM) )
        self._addNode( levelobject.Node(5400,SCREEN_HEIGHT-50) )

        self._addNode( levelobject.Node(5916,SCREEN_HEIGHT-50) )     
        self._addEnemy( enemy.GhoulSlow(5950,500, PLATFORM) )
        self._addNode( levelobject.Node(6000,SCREEN_HEIGHT-50) )

        self._addNode( levelobject.Node(6300,SCREEN_HEIGHT-50) )     
        self._addEnemy( enemy.GhoulSlow(6400,500, PLATFORM) )
        self._addNode( levelobject.Node(6500,SCREEN_HEIGHT-50) )

        self._addNode( levelobject.Node(8300,SCREEN_HEIGHT-50) )     
        self._addTerrain( levelobject.MetroidPlatform(8300,SCREEN_HEIGHT-32) )
        self._addEnemy( enemy.GhoulSlow(8350,500, PLATFORM) )
        self._addNode( levelobject.Node(8500,SCREEN_HEIGHT-50) )

        self._addNode( levelobject.Node(10000,SCREEN_HEIGHT-50) )     
        self._addTerrain( levelobject.MetroidPlatform(10000,SCREEN_HEIGHT-32) )
        self._addEnemy( enemy.GhoulSlow(10150,500, PLATFORM) )
        self._addNode( levelobject.Node(10200,SCREEN_HEIGHT-50) )     

        self._addCheckpoint(10500)
