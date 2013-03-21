import pygame
import os
import sys

from levelobject import LevelObject,StaticImage
import eventmanager
import sound

class StartMenu(object):

    def __init__(self):
        self.level = 0
        
        self.gamma = 1.0

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
        #level select page
        self.lvl_bg        = StaticImage("images/menusprites/levelsel.png",0,0)
        self.lvl1          = StaticImage("images/menusprites/lvl1.png",415,177)
        self.lvl2          = StaticImage("images/menusprites/lvl2.png",415,262)
        self.lvl3          = StaticImage("images/menusprites/lvl3.png",415,347)
        self.lvl4          = StaticImage("images/menusprites/lvl4.png",415,430)
        self.lvl5          = StaticImage("images/menusprites/lvl5.png",415,515)
        self.lvltut        = StaticImage("images/menusprites/tutorial.png",400,93)
        #options page
        self.options_bg          = StaticImage( "images/menusprites/optionsScreen.png",0,0)
        self.volup_button        = StaticImage( "images/menusprites/volumeUp.png",445, 262 )
        self.voldown_button      = StaticImage( "images/menusprites/volumeDown.png",5, 262 )
        self.volupFX_button      = StaticImage( "images/menusprites/volumeUp.png",445, 392 )
        self.voldownFX_button    = StaticImage( "images/menusprites/volumeDown.png",5, 392 )
        self.gammaUp_button      = StaticImage( "images/menusprites/plus.png", 245, 510 )
        self.gammaDown_button    = StaticImage( "images/menusprites/minus.png", 205, 510 )
        self.menublock           = StaticImage( "images/menusprites/menublock.png", 0, 0 )
        self.options_back_button = StaticImage( "images/menusprites/back.png",444, 530 )

        self.bgm = 'sounds/bgm/SureShot.wav'

        self.playing = False
        self.loadLevel = False
        self.show_instructions = False
        self.show_options = False
        self.show_level = False

    def draw(self,camera):

        if not self.show_instructions and not self.show_options and not self.show_level:
            self.splash_bg.draw(camera)
            self.newgame_button.draw(camera)
            self.loadgame_button.draw(camera)
            self.instructions_button.draw(camera)
            self.options_button.draw(camera)
            self.quit_button.draw(camera)

        elif self.show_instructions:
            self.instructions_bg.draw(camera)
            self.back_button.draw(camera)

        elif self.show_options:
            #Options Screen
            self.options_bg.draw(camera)
            self.volup_button.draw(camera)
            self.voldown_button.draw(camera)
            self.volupFX_button.draw(camera)
            self.voldownFX_button.draw(camera)
            self.gammaUp_button.draw(camera)
            self.gammaDown_button.draw(camera)
            self.options_back_button.draw(camera)
            #bgm volume bar
            for i in range(0, sound.get_bgm_vol()):
                self.menublock.rect.topleft = ( 133 + i*self.menublock.rect.width,265 )
                self.menublock.draw(camera)
            #sfx volume bar
            for i in range(0, sound.get_sfx_vol()):
                self.menublock.rect.topleft = ( 133 + i*self.menublock.rect.width,395 )
                self.menublock.draw(camera)
                
        elif self.show_level:
            #Level Select Screen
            self.lvl_bg.draw(camera)
            self.lvltut.draw(camera)
            self.lvl1.draw(camera)
            self.lvl2.draw(camera)
            self.lvl3.draw(camera)
            self.lvl4.draw(camera)
            self.lvl5.draw(camera)

    def update(self):

        evman = eventmanager.get()

        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            #StartMenu
            if not self.show_instructions and not self.show_options and not self.show_level:
                #new game
                if self.newgame_button.get_rect().collidepoint(clickpoint):
                    #self.currentLevel = 0
                    self.show_level = True
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
            elif self.show_options:
                if self.volup_button.get_rect().collidepoint(clickpoint):
                    #clicked bgm vol up
                    sound.set_bgm_vol(sound.get_bgm_vol() + 10)
                    sys.stdout.write('BGM vol: %s\n' % (sound.get_bgm_vol()))
                elif self.voldown_button.get_rect().collidepoint(clickpoint):
                    #clicked bgm vol down
                    sound.set_bgm_vol(sound.get_bgm_vol() - 10)
                    sys.stdout.write('BGM vol: %s\n' % (sound.get_bgm_vol()))
                elif self.volupFX_button.get_rect().collidepoint(clickpoint):
                    #clicked sfx vol up
                    sound.set_sfx_vol(sound.get_sfx_vol() + 10)
                    sound.play_sfx('sounds/SSB_Kick_Hit1.wav')
                    sys.stdout.write('SFX vol: %s\n' % (sound.get_sfx_vol()))
                elif self.voldownFX_button.get_rect().collidepoint(clickpoint):
                    #clicked sfx vol down
                    sound.set_sfx_vol(sound.get_sfx_vol() - 10)
                    sound.play_sfx('sounds/SSB_Kick_Hit1.wav')
                    sys.stdout.write('SFX vol: %s\n' % (sound.get_sfx_vol()))
                elif self.gammaUp_button.get_rect().collidepoint(clickpoint):
                    #clicked gamma up
                    if self.gamma < 2.5:
                        self.gamma = self.gamma + .1
                    pygame.display.set_gamma(self.gamma)
                    sys.stdout.write('Gamma: %s\n' % (self.gamma))
                elif self.gammaDown_button.get_rect().collidepoint(clickpoint):
                    #clicked gamma down
                    if self.gamma > 0.2:
                        self.gamma = self.gamma - .1
                    pygame.display.set_gamma(self.gamma)
                    sys.stdout.write('Gamma: %s\n' % (self.gamma))
                elif self.options_back_button.get_rect().collidepoint(clickpoint):
                    #clicked back
                    self.show_options = False
            #Options Menu
            elif self.show_level:
                if self.lvltut.get_rect().collidepoint(clickpoint):
                    self.setLevel(0)
                elif self.lvl1.get_rect().collidepoint(clickpoint):
                    self.setLevel(1)
                elif self.lvl2.get_rect().collidepoint(clickpoint):
                    self.setLevel(2)
                elif self.lvl3.get_rect().collidepoint(clickpoint):
                    self.setLevel(3)
                elif self.lvl4.get_rect().collidepoint(clickpoint):
                    self.setLevel(4)
                elif self.lvl5.get_rect().collidepoint(clickpoint):
                    self.setLevel(5)
                
            #if on instructions go back to StartMenu
            else:
                if self.back_button.get_rect().collidepoint(clickpoint):
                    if self.show_instructions:
                        self.show_instructions = False
                    elif self.show_options:
                        self.show_options = False
                        
    def isPlaying(self):
        return self.playing

    def setLevel(self, thelevel):
        self.level = thelevel
        self.playing = True
        #logger.get().setChar(thechar)

    def getLevel(self):
        return self.level