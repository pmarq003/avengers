from levelobject import StaticImage
import eventmanager
import sound

class HUD(object):
    def __init__(self):
        self.vol = True

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

    def draw(self,camera):
        self.volume_button = StaticImage( "images/menusprites/volume.png",
                camera.window.right-30, camera.window.top )
        self.mute_button = StaticImage( "images/menusprites/mute.png",
                camera.window.right-30, camera.window.top )

        if self.vol:
            self.volume_button.draw(camera)
        else:
            self.mute_button.draw(camera)

    def getVol(self):
        return self.vol
