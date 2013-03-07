import pygame
import os
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class StartMenu(object):

    def __init__(self):
        self.currentLevel = 0

        self.splash_bg           = StaticImage( "images/menusprites/splash.png",0,0 )
        #StartMenu buttons
        self.newgame_button      = StaticImage( "images/menusprites/newgame.png",460, 304 )
        self.loadgame_button     = StaticImage( "images/menusprites/loadgame.png", 460, 340)
        self.instructions_button = StaticImage( "images/menusprites/instructions.png", 445, 375 )
        self.options_button      = StaticImage( "images/menusprites/options.png",465, 410 )
        self.quit_button         = StaticImage( "images/menusprites/quit.png",480, 445 )
        #instructions page 
        self.instructions_bg     = StaticImage( "images/menusprites/instrScreen.png",0,0 )
        self.back_button         = StaticImage( "images/menusprites/back.png",414, 500 )
        #options page
        self.options_bg          = StaticImage("images/menusprites/optionsScreen.png",0,0)
        self.volup_button         = StaticImage( "images/menusprites/volumeUp.png",460, 304 )
        self.voldown_button         = StaticImage( "images/menusprites/volumeDown.png",460, 340 )

        self.bgm = 'sounds/SureShot.wav'

        self.playing = False
        self.loadLevel = False
        self.show_instructions = False
        self.show_options = False

    def isPlaying(self):
        return self.playing


    def draw(self,camera):

        if not self.show_instructions and not self.show_options:
            self.splash_bg.draw(camera)
            self.newgame_button.draw(camera)
            self.loadgame_button.draw(camera)
            self.instructions_button.draw(camera)
            self.options_button.draw(camera)
            self.quit_button.draw(camera)

        elif self.show_instructions and not self.show_options:
            self.instructions_bg.draw(camera)
            self.back_button.draw(camera)

        elif self.show_options and not self.show_instructions:
            self.options_bg.draw(camera)
            self.volup_button.draw(camera)
            self.voldown_button.draw(camera)
            self.back_button.draw(camera)

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            #StartMenu
            if not self.show_instructions and not self.show_options:
                #new game
                if self.newgame_button.get_rect().collidepoint(clickpoint):
                    self.currentLevel = 1
                    self.playing = True
                #load game
                elif self.loadgame_button.get_rect().collidepoint(clickpoint):
                    if os.path.isfile('save'):
                        self.loadLevel = True

                #options
                elif self.options_button.get_rect().collidepoint(clickpoint):
                    self.show_instructions = False
                    self.show_options = True
                #exit
                elif self.quit_button.get_rect().collidepoint(clickpoint):
                    print("Exiting....")
                    sys.exit(0)

                #isntructions
                elif self.instructions_button.get_rect().collidepoint(clickpoint):
                    self.show_options = False
                    self.show_instructions = True

            #Options Menu
            elif self.show_options and not self.show_instructions:
                if self.volup_button.get_rect().collidepoint(clickpoint):
                    sound.set_bgm_vol(sound.get_bgm_vol() + 0.1)
                    sys.stdout.write('BGM vol: %s\n' % (sound.get_bgm_vol()))
                elif self.voldown_button.get_rect().collidepoint(clickpoint):
                    sound.set_bgm_vol(sound.get_bgm_vol() - 0.1)
                    sys.stdout.write('BGM vol: %s\n' % (sound.get_bgm_vol()))
                elif self.back_button.get_rect().collidepoint(clickpoint):
                    if self.show_instructions:
                        self.show_instructions = False
                    elif self.show_options:
                        self.show_options = False
                    
            #if on instructions go back to StartMenu
            else:
                if self.back_button.get_rect().collidepoint(clickpoint):
                    if self.show_instructions:
                        self.show_instructions = False
                    elif self.show_options:
                        self.show_options = False
