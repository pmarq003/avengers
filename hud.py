from levelobject import StaticImage
import eventmanager
import sound

class HUD(object):
    def __init__(self):
        self.vol = True
        self.time = 0
        self.timeString = "000"

        self.volume_button = StaticImage( "images/menusprites/volume.png", 0, 0 )
        self.mute_button = StaticImage( "images/menusprites/mute.png", 0, 0 )

        self.heart = StaticImage( "images/heart.png", 0, 0 )
        self.sattackbar = StaticImage( "images/sattackbar.png", 0, 0 )
        self.sattackblock = StaticImage( "images/sattackblock.png", 0, 0 )
        
        self.timedigit = StaticImage( "images/hudsprites/0.png", 0, 0 )

    def update(self):
        evman = eventmanager.get()
        if evman.MOUSE1CLICK != False:
            event = evman.MOUSE1CLICK
            clickpoint = event.pos

            if self.volume_button.get_rect().collidepoint(clickpoint):
                self.vol = not self.vol
                if self.vol:
                    sound.set_bgm_vol(100)
                    sound.set_sfx_vol(100)
                else:
                    sound.set_bgm_vol(0)
                    sound.set_sfx_vol(0)

    def drawVol(self,camera):
        if self.vol:
            self.volume_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.volume_button.draw(camera)
        else:
            self.mute_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.mute_button.draw(camera)

    def draw(self,camera,avengers_obj):

        self.drawVol(camera)

        for i in range(0,avengers_obj.player_lives):
            self.heart.rect.topleft = ( camera.window.left + i*( self.heart.rect.width + 10) + 10,
                                        camera.window.top + 10 )
            self.heart.draw(camera)

        self.sattackbar.rect.topleft = camera.window.left + 10, camera.window.top + 55
        self.sattackbar.draw(camera)

        for i in range(0, avengers_obj.currLevel.player.sattack_ammo):
            self.sattackblock.rect.topleft = ( camera.window.left + 13 + i*self.sattackblock.rect.width,
                                               camera.window.top + 58 )
            self.sattackblock.draw(camera)
        
        for i in range(0, len(self.timeString)):
            self.timedigit = StaticImage( "images/hudsprites/%s.png" % self.timeString[i], 
                                          camera.window.right - 100 + i*self.timedigit.rect.width, 
                                          camera.window.top + 58 )
            self.timedigit.draw(camera)
            #sys.stdout.write('String element: %s\n' % timer)
        
    def getVol(self):
        return self.vol
    
    def incTime(self):
        self.time = self.time + 1
        self.timeString = "%03d" % self.time
