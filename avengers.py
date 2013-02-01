import pygame, sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avengers')
red = 255, 0, 0
screen.fill(red)

logo = pygame.image.load('avengers.jpg')
logorect = logo.get_rect()

while True:
	for event in pygame.event.get():

		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos
		elif event.type == MOUSEBUTTONUP:
			mousex,mousty =event.pos

		elif event.type == KEYDOWN:
			if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
				msg = 'arrow key pressed'
			if event.key == K_a:
				msg = '"A: key pressed'
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))

screen.blit(logo, logorect)
pygame.display.flip()
clock.tick(30)