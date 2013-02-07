import pygame
import player
import image
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Level(object):

    #Should be overwritten by child classes
    def __init__(self):
        self.player = None
        self.background = None
        pass

    def update(self): 
        self.player.update() 

    def draw(self,camera):
        if self.background:
            self.background.draw(camera)
        self.player.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

class Level1(Level):

    def __init__(self):
        self.player = player.CaptainAmerica(0,0)
        self.background = image.StaticImage('images/300x300logo.jpg',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
