import pygame
import player

class Level(object):

    #Should be overwritten by child classes
    def __init__(self):
        self.player = None
        pass

    def update(self): 
        self.player.update() 

    def draw(self,screen):
        self.player.draw(screen)

class Level1(Level):

    def __init__(self):
        self.player = player.CaptainAmerica(0,0)
