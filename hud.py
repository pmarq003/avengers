'''
Created on Feb 23, 2013

@author: Owner
'''
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
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class HUD(object):
    '''
    classdocs
    '''


    def __init__(self):
#        self.volume_button = StaticImage( "images/menusprites/volume.png",       970, 0   )
#        self.mute_button = StaticImage( "images/menusprites/mute.png",         970, 0   )
        
        self.vol = True
        
    def update(self):
        evman = eventmanager.get()
        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            if self.volume_button.get_rect().collidepoint(clickpoint):
                self.vol = not self.vol
                
    def draw(self,camera):
        
        
        self.volume_button = StaticImage( "images/menusprites/volume.png",
                camera.window.right-30, camera.window.top )
        self.mute_button = StaticImage( "images/menusprites/mute.png",
                camera.window.right-30, camera.window.top )
        
        if self.vol:
            self.volume_button.draw(camera)
            sound.set_bgm_vol(100)
            sound.set_sfx_vol(100)
        else:
            self.mute_button.draw(camera)
            sound.set_bgm_vol(0)
            sound.set_sfx_vol(0)
            
    def getVol(self):
        return self.vol