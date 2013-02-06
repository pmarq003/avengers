import pygame
import eventmanager
from pygame.sprite import Sprite

class Player(Sprite):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    message = "hello world"

    def __init__(self, x, y):
        self.position.topleft = (x,y)

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

    def draw(self,screen):
        screen.blit(self.image, self.position)
        
class CaptainAmerica(Player):
    image = pygame.image.load('images/Captain_America_FB_Artwork_3.png')
    position = image.get_rect()
    message = "I am Captain America!"
