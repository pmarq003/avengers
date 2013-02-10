import pygame
import levelobject
import time

from pygame.locals import *
from pygame.sprite import Sprite
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Avengers - Six Guys')

#splash screen
splash = pygame.Surface(screen.get_size())
splash = splash.convert()
splash.fill((0,0,0))
x, y = screen.get_size()
screen.blit(splash, (0, 0))
logo = pygame.image.load("images/splash.png").convert_alpha()
screen.blit(logo, (0,0))
pygame.display.update()

startbutton = pygame.Surface((112,22), pygame.SRCALPHA, 32)
startbutton = startbutton.convert_alpha()
screen.blit(startbutton, (369,363))
button0 = pygame.image.load("images/menusprites/startgame.png")
screen.blit(button0,(369,363))

instructions = pygame.Surface((115,22), pygame.SRCALPHA, 32)
instructions = instructions.convert_alpha()
screen.blit(instructions, (367,393))
button1 = pygame.image.load("images/menusprites/instructions.png")
screen.blit(button1,(367,393))

options = pygame.Surface((85,22), pygame.SRCALPHA, 32)
options = options.convert_alpha()
screen.blit(options, (383,423))
button2 = pygame.image.load("images/menusprites/options.png")
screen.blit(button2,(383,423))

quit = pygame.Surface((112,22), pygame.SRCALPHA, 32)
quit = quit.convert_alpha()
screen.blit(quit, (371, 453))
button3 = pygame.image.load("images/menusprites/quit.png")
screen.blit(button3,(371,453))

volume = pygame.Surface((25,25), pygame.SRCALPHA, 32)
volume = volume.convert_alpha()
screen.blit(volume, (970, 0))
button4 = pygame.image.load("images/menusprites/volume.png")
screen.blit(button4,(970,0))
pygame.display.update()

playing = False

while(not pygame.event.peek(pygame.MOUSEBUTTONDOWN)):
	pygame.event.wait()

for event in pygame.event.get():
	if event.type == MOUSEBUTTONDOWN:
		if event.button == 1:

			srect = pygame.Rect(369,363,112,22)
			playing = srect.collidepoint(pygame.mouse.get_pos())

			irect = pygame.Rect(367,393,115,22)
			loadinstr = irect.collidepoint(pygame.mouse.get_pos())

			orect = pygame.Rect(383,423,85,22)
			loadoptions = orect.collidepoint(pygame.mouse.get_pos())

			qrect = pygame.Rect(371,453,112,22)
			quitz = qrect.collidepoint(pygame.mouse.get_pos())

			vrect = pygame.Rect(970,0,25,25)
			mute = srect.collidepoint(pygame.mouse.get_pos())
