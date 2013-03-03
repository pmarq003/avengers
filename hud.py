from levelobject import StaticImage
import eventmanager
import sound

class HUD(object):
    def __init__(self):
        self.vol = True

        self.volume_button = StaticImage( "images/menusprites/volume.png", 0, 0 )
        self.mute_button = StaticImage( "images/menusprites/mute.png", 0, 0 )

        self.heart = StaticImage( "images/heart.png", 0, 0 )

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

    def draw(self,camera,avengers_obj):

        if self.vol:
            self.volume_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.volume_button.draw(camera)
        else:
            self.mute_button.rect.topleft = ( camera.window.right - 30, camera.window.top )
            self.mute_button.draw(camera)

        for i in range(0,avengers_obj.player_lives):
            self.heart.rect.topleft = ( camera.window.left + i*( self.heart.rect.width + 10) + 10,
                                        camera.window.top + 10 )
            self.heart.draw(camera)
        

    def getVol(self):
        return self.vol
