import os, sys

from player import CaptainAmerica

import pygame
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

player1 = CaptainAmerica(SCREEN_HEIGHT - 100)

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

		elif event.type == KEYDOWN and event.key == K_LEFT:
			direction = 3
			screen.fill(bgcolor)
			player1.move(direction)
			msg = player1.message
		elif event.type == KEYDOWN and event.key == K_RIGHT:
			direction = 1
			screen.fill(bgcolor)
			player1.move(direction)
			msg = player1.message
		elif event.type == KEYDOWN and event.key == K_UP:
			direction = 4
			screen.fill(bgcolor)
			player1.move(direction)
			msg = player1.message
		elif event.type == KEYDOWN and event.key == K_DOWN:
			direction = 2
			screen.fill(bgcolor)
			player1.move(direction)
			msg = player1.message
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			sys.exit()		

	screen.blit(logo, logorect)
	screen.blit(player1.image, player1.position)
	pygame.display.flip()
clock.tick(30)
