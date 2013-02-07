import pygame
import player

class Level(object):

    #Should be overwritten by child classes
    def __init__(self):
        self.player = None
        pass

    def update(self): 
        self.player.update() 

    def draw(self,camera):
        self.player.draw(camera)

    def get_player_rect(self):
        return self.player.get_rect()

class Level1(Level):

    def __init__(self):
        self.player = player.CaptainAmerica(0,0)
