import pygame
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class CharSel(object):

    def __init__(self):

        self.splash_bg     = StaticImage( "images/charsel.png",                   0,   0   )
        self.hulk          = StaticImage( "images/hulk/hulkselect.png",    466, 200 )
        self.america       = StaticImage( "images/america/america_select.png", 200, 358 )
        self.mario         = StaticImage( "images/mario/jump_right.gif",      200, 251 )
        self.luigi         = StaticImage( "images/luigi/jump_left.gif",         675, 251 )
        self.ironman       = StaticImage( "images/ironman/ironman_select.png",       440, 580   )
        self.thor          = StaticImage( "images/thor/norm_attack_left.gif",         603, 339   )
        self.back          = StaticImage( "images/back.png",                     414, 500 )
        self.volume_button = StaticImage( "images/menusprites/volume.png",       970, 0   )
        self.mute_button   = StaticImage( "images/menusprites/mute.png",         970, 0   )

        self.bgm = 'sounds/SureShot.wav'

    def draw(self,camera):

            self.splash_bg.draw(camera)
            self.hulk.draw(camera)
            self.america.draw(camera)
            self.mario.draw(camera)
            self.luigi.draw(camera)
            self.ironman.draw(camera)
            self.thor.draw(camera)
            self.back.draw(camera)

            if self.vol:
                self.volume_button.draw(camera)
                sound.set_bgm_vol(100)
                sound.set_sfx_vol(100)
            else:
                self.mute_button.draw(camera)
                sound.set_bgm_vol(0)
                sound.set_sfx_vol(0)

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            if self.hulk.get_rect().collidepoint(clickpoint):
                self.setChar(hulk)

            elif self.mario.get_rect().collidepoint(clickpoint):
                self.setChar(mario)

            elif self.luigi.get_rect().collidepoint(clickpoint):
                self.setChar(luigi)

            elif self.thor.get_rect().collidepoint(clickpoint):
                self.setChar(thor)
                thor
            elif self.america.get_rect().collidepoint(clickpoint):
                self.setChar(america)

            elif self.ironman.get_rect().collidepoint(clickpoint):
                self.setChar(ironman)

    def setChar(self, thechar):
        char = thechar

    def getChar(self):
        return self.char