import pygame
import time
import sys

from pygame.locals import *
from pygame.sprite import Sprite
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Button:
    def __init__(self, left, top, width, height, img):
        self.left = left
        self.top =top
        self.width = width
        self.height = height
        self.img = img
        button = pygame.Surface((width,height), pygame.SRCALPHA, 32)
        button = button.convert_alpha()
        screen.blit(button, (left,top))
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.topleft = (left,top)
        screen.blit(self.image,(left,top))

    def get_rect(self):
        return self.rect 

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Avengers - Six Guys')

#splash screen
splash = pygame.Surface(screen.get_size())
splash = splash.convert()
splash.fill((0,0,0))
x, y = screen.get_size()
screen.blit(splash, (0, 0))
image = pygame.image.load("images/splash.png").convert_alpha()
screen.blit(image, (0,0))
pygame.display.update()

start = Button(369, 363, 122, 22, "images/menusprites/startgame.png")
instructions = Button(367, 393, 115, 22, "images/menusprites/instructions.png")
options = Button(383, 423, 85, 22, "images/menusprites/options.png")
quit = Button(371, 453, 122, 22, "images/menusprites/quit.png")
volume = Button(970, 0, 25, 25, "images/menusprites/volume.png")
pygame.display.update()

playing = False
vol = True

while(not playing):
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if start.get_rect().collidepoint(pygame.mouse.get_pos()):
                    playing = True

                elif instructions.get_rect().collidepoint(pygame.mouse.get_pos()):
                    image = pygame.image.load("images/instructions.png")
                    screen.blit(image, (0,0))
                    back = Button(414, 500, 173, 22, "images/back.png")
                    pygame.display.update()
                    done = False
                    while(not done):
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONDOWN:
                                if back.get_rect().collidepoint(pygame.mouse.get_pos()):
                                    image = pygame.image.load("images/splash.png").convert_alpha()
                                    screen.blit(image, (0,0))
                                    start = Button(369, 363, 122, 22, "images/menusprites/startgame.png")
                                    instructions = Button(367, 393, 115, 22, "images/menusprites/instructions.png")
                                    options = Button(383, 423, 85, 22, "images/menusprites/options.png")
                                    quit = Button(371, 453, 122, 22, "images/menusprites/quit.png")
                                    volume = Button(970, 0, 25, 25, "images/menusprites/volume.png")
                                    pygame.display.update()
                                    done = True

                elif options.get_rect().collidepoint(pygame.mouse.get_pos()):
                    print "options hit"

                elif quit.get_rect().collidepoint(pygame.mouse.get_pos()):
                    sys.exit(0)

                elif volume.get_rect().collidepoint(pygame.mouse.get_pos()):
                    vol = not vol
                    if not vol:
                        screen.blit(image, (0,0))
                        mute = Button(970, 0, 25, 25, "images/menusprites/mute.png")
                        start = Button(369, 363, 122, 22, "images/menusprites/startgame.png")
                        instructions = Button(367, 393, 115, 22, "images/menusprites/instructions.png")
                        options = Button(383, 423, 85, 22, "images/menusprites/options.png")
                        quit = Button(371, 453, 122, 22, "images/menusprites/quit.png")
                        pygame.display.update()

                    elif vol:
                        screen.blit(image, (0,0))
                        volume = Button(970, 0, 25, 25, "images/menusprites/volume.png")
                        start = Button(369, 363, 122, 22, "images/menusprites/startgame.png")
                        instructions = Button(367, 393, 115, 22, "images/menusprites/instructions.png")
                        options = Button(383, 423, 85, 22, "images/menusprites/options.png")
                        quit = Button(371, 453, 122, 22, "images/menusprites/quit.png")
                        pygame.display.update()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit(0)
