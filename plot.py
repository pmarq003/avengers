import pygame
import sys
import logger

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class Plot(object):

    def __init__(self,currLevel):
        self.currentLevel = 0
        self.plotfolder = "tut"
        self.maxPlot = 1
        
        #only set the level during init, doesn't have to update every time
        if currLevel == 1:    #Super Mario World
            self.plotfolder = "smw"
            self.maxPlot = 15
        elif currLevel == 2:  #Sonic World
            self.plotfolder = "sonic"
            self.maxPlot = 1
        elif currLevel == 3:  #Megaman World
            self.plotfolder = "megaman"
            self.maxPlot = 2
        elif currLevel == 4:  #Metroid World
            self.plotfolder = "metroid"
            self.maxPlot = 2
        elif currLevel == 5:  #Castlevania World
            self.plotfolder = "castlevania"
            self.maxPlot = 2    
        
        self.currentPlot = 1

        self.plotOver = False
        #self.camera = None

        #plot page
        self.plot_back_button    = StaticImage( "images/menusprites/back.png",904, 490 )
        self.plot_next_button    = StaticImage( "images/menusprites/next.png",900, 530 )
        self.plot_skip_button    = StaticImage( "images/menusprites/skip.png",900, 450 )
        self.plot_bg             = StaticImage( "images/plot/smw/1.jpg",0,0)

        #self.bgm = 'sounds/SureShot.wav'
        
        #Mute button
        self.vol = True
        #Remember where the volume was after un-muting
        self.bgm_vol = sound.get_bgm_vol()
        self.sfx_vol = sound.get_sfx_vol()
        
        self.volume_button = StaticImage("images/menusprites/volume.png",960,10)
        self.mute_button   = StaticImage("images/menusprites/mute.png",960,10)

    def draw(self,camera):
#        if self.camera == None:
#            self.camera = camera

#        self.volume_button = StaticImage("images/menusprites/volume.png",camera.window.right-30,camera.window.top+10)
#        self.mute_button   = StaticImage("images/menusprites/mute.png",camera.window.right-30,camera.window.top+10)

        self.plot_bg = StaticImage( "images/plot/%s/%s.jpg" % (self.plotfolder, self.currentPlot),0,0)
        self.plot_bg.draw(camera)
        self.plot_skip_button.draw(camera)
        self.plot_back_button.draw(camera)
        self.plot_next_button.draw(camera)
        
        #Mute button
        if self.vol:
            #self.volume_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.volume_button.draw(camera)
        else:
            #self.mute_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.mute_button.draw(camera)

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos
            #clickpoint = (camera.window.left+clickpoint[0],camera.window.top+clickpoint[1])

            if self.volume_button.get_rect().collidepoint(clickpoint):
                self.vol = not self.vol
                if self.vol:
                    sound.set_bgm_vol(self.bgm_vol)
                    sound.set_sfx_vol(self.sfx_vol)
                else:
                    #update the volume before muting
                    self.bgm_vol = sound.get_bgm_vol()
                    self.sfx_vol = sound.get_sfx_vol()
                    sound.set_bgm_vol(0)
                    sound.set_sfx_vol(0)

#            else
#                self.playing = True
                  
            if self.plot_skip_button.get_rect().collidepoint(clickpoint):
                self.plotOver = True
            elif self.plot_next_button.get_rect().collidepoint(clickpoint) and self.currentPlot < self.maxPlot:
                self.currentPlot = self.currentPlot + 1
            elif self.plot_back_button.get_rect().collidepoint(clickpoint) and self.currentPlot > 1:
                self.currentPlot = self.currentPlot - 1
            elif self.plot_back_button.get_rect().collidepoint(clickpoint) and self.currentPlot == 1:
                pass
            elif self.plot_next_button.get_rect().collidepoint(clickpoint) and self.currentPlot == self.maxPlot:
                self.plotOver = True
                
    def getPlot(self):
        return self.plotOver