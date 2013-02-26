import pygame
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class PauseMenu(object):

    def __init__(self):

        self.camera = None

        #self.bgm = 'sounds/SureShot.wav'

    def draw(self,camera):
        if self.camera == None:
            self.camera = camera

        #to center: x:camera window + window width/2 - img width
        self.bgIm = StaticImage("images/pauseScreen.png",camera.window.left+500-149,camera.window.top+300-218)
        self.resumeIm = StaticImage("images/menusprites/resume.png",camera.window.left+500-52,camera.window.top+300-70)
        #self.restartIm = StaticImage("images/menusprites/restart.png",camera.window.left+500-57,camera.window.top+300-10)
        self.quitIm = StaticImage("images/menusprites/quitt.png",camera.window.left+500-32,camera.window.top+300+50)

        self.bgIm.draw(camera)
        self.resumeIm.draw(camera)
        #self.restartIm.draw(camera)
        self.quitIm.draw(camera)


    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos
            clickpoint = (self.camera.window.left+clickpoint[0],self.camera.window.top+clickpoint[1])
            if self.resumeIm.get_rect().collidepoint(clickpoint):
                eventmanager.get().togglePause()
            #elif self.restartIm.get_rect().collidepoint(clickpoint):
            elif self.quitIm.get_rect().collidepoint(clickpoint):
                pygame.quit()
                sys.exit(0)
