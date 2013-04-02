import charsel
import plot
import pygame
import pygame.sprite
import player
import physics
import enemy
import levelobject
from constants import *
from levelobject import LevelObject,StaticImage
import eventmanager
from parallax import Parallax
import startmenu
import sound
import score


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
        self.levelNumber = -1   #override in specific levels
        self.charsel = charsel.CharSel()
        self.charSelected = False
  #      self.plot = plot.Plot(-1)
        self.plotOver = False
        self._terrain = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()
        self._nodes = pygame.sprite.Group()
        self._entities = pygame.sprite.Group()
        self._hearts = pygame.sprite.Group()
        self._ammo = pygame.sprite.Group()
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
                if self.player.has_star:
                    if enemy.alive:
                        score.get().incScore(30)
                    enemy.die()
                else:
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

            heartCollisions = pygame.sprite.spritecollide(self.player,self._hearts,False)
            for heart in heartCollisions:
                self.gameObj.player_lives += 1
                heart.kill()

            ammoCollisions = pygame.sprite.spritecollide(self.player,self._ammo,False)
            for ammo in ammoCollisions:
                self.player.incAmmo()
                ammo.kill()
                
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
            for nodeObj in self._nodes:
                nodeObj.draw(camera)

            for heartObj in self._hearts:
                heartObj.draw(camera)

            for ammoObj in self._ammo:
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

    def _addAmmo(self,ammoObj):
        self._ammo.add(ammoObj)
    
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
    Tutorial level
"""

class Level0(Level):

    def __init__(self,gameObj):
        Level.__init__(self,gameObj)

        #level number
        self.levelNumber = 0
        self.plot = plot.Plot(self.levelNumber)

        self.height = SCREEN_HEIGHT
        #default player to init enemies TODO doesn't update position...
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
        #default player to init enemies TODO doesn't update position...
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

        self._addNode( levelobject.Node(100, 200) )
        self._addEnemy( enemy.ParaKoopa(700, 200, FLYHORIZ) )
        self._addNode( levelobject.Node(900, 200) )

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
            #movable platform + enemies on clouds
        self._addNode( levelobject.Node(5200,300,0,0,-1))
        self._addTerrain( levelobject.MarioMovablePlatform(5400,300, 5) )
        self._addTerrain( levelobject.MarioCloud(5600,200) )
        self._addEnemy( enemy.Fuzzy(5660, 100, JUMP) )
        self._addTerrain( levelobject.MarioCloud(6200,200) )
        self._addEnemy( enemy.Fuzzy(6260, 100, JUMP) )
        self._addNode( levelobject.Node(6700,300,0,0,-1))
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

        self._addNode( levelobject.Node(11000,-100,0,0,0,-1) )
        self._addTerrain( levelobject.MarioMovablePlatform(11000,0,0,5) )
        self._addNode( levelobject.Node(11000,400,0,0,0,-1) )
            #floor
        self._addTerrain( levelobject.Checkpoint(11350,SCREEN_HEIGHT-153) )
        self._addCheckpoint(11300)
        self._addTerrain( levelobject.MarioGround1632(11300,SCREEN_HEIGHT-16) )

        self._addEnemy( enemy.ShyGuy(12700,400, FLOOR) )

        self._addTerrain( levelobject.MarioGround1632(12932,SCREEN_HEIGHT-16) )
        self._addTerrain( levelobject.MarioCastle(12700,SCREEN_HEIGHT-338) )

        #self._addHeart( levelobject.Heart(1000,300) )
        #self._addAmmo( levelobject.Ammo(700,300) )
        #self._addStar( levelobject.Star(1300, 150) )

            #temp end of level
        self._addCheckpoint(12500)


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
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl2.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/sonic/background.jpg',0,-55)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)
        
        #sonics
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.Sonic(700,400, PLATFORM) )
        self._addEnemy( enemy.Sonic(900,400, PLATFORM) )
        self._addEnemy( enemy.Sonic(1200,400, PLATFORM) )
        self._addNode( levelobject.Node(1500,550) )
        
        self._addCheckpoint(1000)

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
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl3.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/megaman/background.png',0,-55)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)
        
        #Megamans
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.BoyRobot1(700,400, PLATFORM) )
        self._addEnemy( enemy.BoyRobot1(900,400, PLATFORM) )
        self._addEnemy( enemy.BoyRobot1(1200,400, PLATFORM) )
        self._addNode( levelobject.Node(1500,550) )
        
        self._addCheckpoint(1000)


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
        #default player to init enemies TODO doesn't update position...
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
        #self._addEnemy( enemy.SpacePirate(700,400, PLATFORM) )
        #self._addEnemy( enemy.SpacePirate(800,400, PLATFORM) )
        #self._addEnemy( enemy.SpacePirate(900,400, PLATFORM) )
        self._addNode( levelobject.Node(1000,550) )

        self._addHeart( levelobject.Heart(1200,550) )

        self._addNode( levelobject.Node(900,380) )
        self._addTerrain( levelobject.MetroidPlatform(900,400) )
        #self._addEnemy( enemy.Metroid(950,350, PLATFORM) )
        self._addNode( levelobject.Node(900+256,380) )

        self._addNode( levelobject.Node(1300,230) )
        self._addTerrain( levelobject.MetroidPlatform(1300,250) )
        #self._addEnemy( enemy.Metroid(1350,200, PLATFORM) )
        #self._addEnemy( enemy.Metroid(1450,200, PLATFORM) )
        self._addNode( levelobject.Node(1300+256,230) )

        self._addNode( levelobject.Node(1700,80) )
        self._addTerrain( levelobject.MetroidPlatform(1700,100) )
        #self._addEnemy( enemy.Metroid(1750,50, PLATFORM) )
        #self._addEnemy( enemy.Metroid(1800,50, PLATFORM) )
        #self._addEnemy( enemy.Metroid(1850,50, PLATFORM) )
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
        #self._addEnemy( enemy.SpacePirate(2350,500, PLATFORM) )
        self._addNode( levelobject.Node(2300+256,530) )

        self._addNode( levelobject.Node(2800,530) )
        self._addTerrain( levelobject.MetroidPlatform(2800, 550) )
        #self._addEnemy( enemy.SpacePirate(2850,500, PLATFORM) )
        self._addNode( levelobject.Node(2800+256,530) )

        self._addNode( levelobject.Node(3300,530) )
        self._addTerrain( levelobject.MetroidPlatform(3300, 550) )
        #self._addEnemy( enemy.SpacePirate(3350,500, PLATFORM) )
        self._addNode( levelobject.Node(3300+256,530) )

        self._addNode( levelobject.Node(3800,530) )
        self._addTerrain( levelobject.MetroidPlatform(3800, 550) )
        #self._addEnemy( enemy.SpacePirate(3850,500, PLATFORM) )
        self._addNode( levelobject.Node(3800+256,530) )


        #Second level pyramid
        self._addNode( levelobject.Node(3050,330) )
        self._addTerrain( levelobject.MetroidPlatform(3050, 350) )
        #self._addEnemy( enemy.SpacePirate(3100,300, PLATFORM) )
        self._addNode( levelobject.Node(3050+256,330) )

        self._addNode( levelobject.Node(3550,330) )
        self._addTerrain( levelobject.MetroidPlatform(3550, 350) )
        #self._addEnemy( enemy.SpacePirate(3600,300, PLATFORM) )
        self._addNode( levelobject.Node(3550+256,330) )

        #Top of pyramid
        self._addTerrain( levelobject.MetroidPlatform(3300, 150) )

        #Going up
        self._addNode( levelobject.Node(3700,200,0,0,-1,-1) )
        self._addTerrain( levelobject.MetroidMovablePlatform( 3600, 150, 0, 5 ) )
        self._addNode( levelobject.Node(3700,-500,0,0,-1,-1) )

        self._addNode( levelobject.Node(200,500) )
        self._addEnemy( enemy.FastMetroid(600,500, PLATFORM) )
        self._addEnemy( enemy.FastMetroid(700,500, PLATFORM) )
        self._addEnemy( enemy.FastMetroid(800,500, PLATFORM) )
        self._addNode( levelobject.Node(200,500) )

        #Ammo cache off to the right of the pyramid
        self._addNode( levelobject.Node(4500,530) )
        self._addTerrain( levelobject.MetroidPlatform(4500, 550) )
        self._addAmmo( levelobject.Ammo( 4550, 530 ) )
        self._addAmmo( levelobject.Ammo( 4550+50, 530 ) )
        self._addAmmo( levelobject.Ammo( 4550+100, 530 ) )
        self._addNode( levelobject.Node(4500+256,530) )

        self._addCheckpoint(10000)


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
        #default player to init enemies TODO doesn't update position...
        self.player = player.IronMan(100,100,self)

        #background music
        self.bgm = 'sounds/bgm/lvl5.wav'

        #background
        self.background = levelobject.StaticImage('images/levelsprites/castlevania/background.jpg',0,-55)
        self.parallax = False

        #level objects in order
            #floor + checkpoint
        self._addTerrain( levelobject.MarioGround1632(0,SCREEN_HEIGHT-32) )
        self._addCheckpoint(0)
        
        #Ghouls
        self._addNode( levelobject.Node(20,550) )
        self._addEnemy( enemy.Ghoul(700,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(900,400, PLATFORM) )
        self._addEnemy( enemy.Ghoul(1200,400, PLATFORM) )
        self._addNode( levelobject.Node(1500,550) )
        
        self._addCheckpoint(1000)
