import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite
#from vec2d import vec2d

from pygame.locals import *

#initialize pygame lib
pygame.init()
#clock used for fps
clock = pygame.time.Clock()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
#creates window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avengers')
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255
black = 0, 0, 0
bgcolor = 36, 48, 59
screen.fill(bgcolor)

logo = pygame.image.load('300x300logo.jpg')
logorect = logo.get_rect()
toCenter = 150
logorect.topleft = (SCREEN_WIDTH/2-toCenter,SCREEN_HEIGHT/2-toCenter)

fontObj = pygame.font.Font('freesansbold.ttf', 100)
msg = 'Avengers'

while True:
	msgSurface = fontObj.render(msg, False, black)
	msgRect = msgSurface.get_rect()
	msgRect.topleft = (0,0)
	screen.blit(msgSurface, msgRect)
	for event in pygame.event.get():

		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos

		elif event.type == MOUSEBUTTONDOWN:
			screen.fill(bgcolor)

			mousex,mousty =event.pos
			msg = 'mouse button down'

		elif event.type == KEYDOWN:
			screen.fill(bgcolor)

			if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
				msg = 'arrow key pressed'
			if event.key == K_a:
				msg = '"A" key pressed'
			if event.key == K_ESCAPE:
				sys.exit()

	screen.blit(logo, logorect)
	pygame.display.flip()
clock.tick(30)