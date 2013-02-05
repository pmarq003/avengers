import pygame
from pygame.sprite import Sprite

class Player(pygame.sprite.Sprite):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    message = "hello world"
    def __init__(self, SCREEN_HEIGHT):
        self.message = msg
        self.position.topleft = (0,SCREEN_HEIGHT)
        
class CaptainAmerica(Player):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    def __init__(self, SCREEN_HEIGHT):
        self.message = "I am Captain America!"
        self.position.topleft = (0,SCREEN_HEIGHT)
    def move(self, direction):
        if(direction == 1):
            self.message = "Moved Right"
            self.position = self.position.move(10,0)
        elif(direction == 2):
            self.message = "Moved Down"
            self.position = self.position.move(0,10)
        elif(direction == 3):
            self.message = "Moved Left"
            self.position = self.position.move(-10,0)
        elif(direction == 4):
            self.message = "Moved Up"
            self.position = self.position.move(0,-10)