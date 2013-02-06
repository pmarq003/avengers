import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(pygame.sprite.Sprite):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    message = "hello world"

    def __init__(self, SCREEN_HEIGHT):
        self.message = msg
        self.position.topleft = (0,SCREEN_HEIGHT)

    def update(self):
        evman = eventmanager.get()
        if evman.UPPRESSED:
            self.message = "Moved Up"
            self.position = self.position.move(0,-10)

        elif evman.DOWNPRESSED:
            self.message = "Moved Down"
            self.position = self.position.move(0,10)

        elif evman.LEFTPRESSED:
            self.message = "Moved Left"
            self.position = self.position.move(-10,0)

        elif evman.RIGHTPRESSED:
            self.message = "Moved Right"
            self.position = self.position.move(10,0)
        
class CaptainAmerica(Player):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    def __init__(self, SCREEN_HEIGHT):
        self.message = "I am Captain America!"
        self.position.topleft = (0,SCREEN_HEIGHT)
