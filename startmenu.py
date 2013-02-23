import pygame
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class StartMenu(object):

    def __init__(self):

        self.splash_bg           = StaticImage( "images/splash.png",                   0,   0   )
        self.start_button        = StaticImage( "images/menusprites/startgame.png",    369, 363 )
        self.instructions_button = StaticImage( "images/menusprites/instructions.png", 367, 393 )
        self.options_button      = StaticImage( "images/menusprites/options.png",      383, 423 )
        self.quit_button         = StaticImage( "images/menusprites/quit.png",         371, 453 )
        self.volume_button       = StaticImage( "images/menusprites/volume.png",       970, 0   )
        self.mute_button         = StaticImage( "images/menusprites/mute.png",         970, 0   )

        self.instructions_bg     = StaticImage( "images/instructions.png",             0,   0   )
        self.back_button         = StaticImage( "images/back.png",                     414, 500 )
        
        self.bgm = 'sounds/SureShot.wav'
        
        self.playing = False
        self.vol = True
        self.show_instructions = False

    def isPlaying(self):
        return self.playing

    def draw(self,camera):
        
        if not self.show_instructions:
            self.splash_bg.draw(camera)
            self.start_button.draw(camera)
            self.instructions_button.draw(camera)
            self.options_button.draw(camera)
            self.quit_button.draw(camera)

            if self.vol:
                self.volume_button.draw(camera)
                sound.set_bgm_vol(100)
                sound.set_sfx_vol(100)
            else:
                self.mute_button.draw(camera)
                sound.set_bgm_vol(0)
                sound.set_sfx_vol(0)

        else:
            self.instructions_bg.draw(camera)
            self.back_button.draw(camera)

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            if not self.show_instructions:
                if self.start_button.get_rect().collidepoint(clickpoint):
                    self.playing = True

                elif self.options_button.get_rect().collidepoint(clickpoint):
                    print("options hit")

                elif self.quit_button.get_rect().collidepoint(clickpoint):
                    print("Exiting....")
                    sys.exit(0)

                elif self.volume_button.get_rect().collidepoint(clickpoint):
                    self.vol = not self.vol

                elif self.instructions_button.get_rect().collidepoint(clickpoint):
                    self.show_instructions = True

            else:
                if self.back_button.get_rect().collidepoint(clickpoint):
                        self.show_instructions = False
