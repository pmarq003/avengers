import pygame
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class CharSel(object):

    def __init__(self):

        self.char = 0
        self.camera = None

        #self.bgm = 'sounds/SureShot.wav'

    def draw(self,camera):
        if self.camera == None:
            self.camera = camera

        self.splash_bg     = StaticImage("images/charsel.png",camera.window.left, camera.window.top)
        self.hulk          = StaticImage("images/hulk/hulkselect.png",camera.window.left+220,300+camera.window.top)
        self.america       = StaticImage("images/america/america_select.png",camera.window.left+550,300+camera.window.top)
        self.ironman       = StaticImage("images/ironman/ironman_select.png",camera.window.left+350,300+camera.window.top)
        self.thor          = StaticImage("images/thor/norm_attack_left.gif",camera.window.left+700,300+camera.window.top)
        self.volume_button = StaticImage("images/menusprites/volume.png",camera.window.right-30,camera.window.top+10)
        self.mute_button   = StaticImage("images/menusprites/mute.png",camera.window.right-30,camera.window.top+10)

        self.splash_bg.draw(camera)
        self.hulk.draw(camera)
        self.america.draw(camera)
        self.ironman.draw(camera)
        self.thor.draw(camera)

        """
        if self.vol:
            self.volume_button.draw(camera)
            sound.set_bgm_vol(100)
            sound.set_sfx_vol(100)
        else:
            self.mute_button.draw(camera)
            sound.set_bgm_vol(0)
            sound.set_sfx_vol(0)
            """

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos
            clickpoint = (self.camera.window.left+clickpoint[0],self.camera.window.top+clickpoint[1])
            if self.hulk.get_rect().collidepoint(clickpoint):
                self.setChar(1)

            elif self.thor.get_rect().collidepoint(clickpoint):
                self.setChar(2)

            elif self.america.get_rect().collidepoint(clickpoint):
                self.setChar(3)

            elif self.ironman.get_rect().collidepoint(clickpoint):
                self.setChar(4)

    def setChar(self, thechar):
        self.char = thechar

    def getChar(self):
        return self.char
