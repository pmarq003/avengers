import pygame
import player
import image
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Level(object):

    def update(self): 
        self.player.update() 

        #Make sure player doesn't go above or below map. Remember y-axis goes down
        if self.player.rect.bottom > self.height:
            self.player.rect.bottom = self.height
            self.player.stallY()
            self.player.canJump = True
        elif self.player.rect.top < 0:
            self.player.rect.top = 0
            self.player.stallY()

    def draw(self,camera):
        if self.background:
            self.background.draw(camera)
        self.player.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

class Level1(Level):
    height = SCREEN_HEIGHT
    player = player.CaptainAmerica(0,0)
    background = image.StaticImage('images/300x300logo.jpg',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
