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
		image = pygame.image.load(img)
		screen.blit(image,(left,top))

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
				if pygame.Rect(start.left, start.top, start.width, start.height).collidepoint(pygame.mouse.get_pos()):
					playing = True
					print "start hit"

				elif pygame.Rect(instructions.left, instructions.top, instructions.width, instructions.height).collidepoint(pygame.mouse.get_pos()):
					image = pygame.image.load("images/instructions.png")
					screen.blit(image, (0,0))
					back = Button(414, 500, 173, 22, "images/back.png")
					pygame.display.update()
					done = False
					while(not done):
						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN:
								if pygame.Rect(back.left, back.top, back.width, back.height).collidepoint(pygame.mouse.get_pos()):
									image = pygame.image.load("images/splash.png").convert_alpha()
									screen.blit(image, (0,0))
									start = Button(369, 363, 122, 22, "images/menusprites/startgame.png")
									instructions = Button(367, 393, 115, 22, "images/menusprites/instructions.png")
									options = Button(383, 423, 85, 22, "images/menusprites/options.png")
									quit = Button(371, 453, 122, 22, "images/menusprites/quit.png")
									volume = Button(970, 0, 25, 25, "images/menusprites/volume.png")
									pygame.display.update()
									done = True

				elif pygame.Rect(options.left, options.top, options.width, options.height).collidepoint(pygame.mouse.get_pos()):
					print "options hit"

				elif pygame.Rect(quit.left, quit.top, quit.width, quit.height).collidepoint(pygame.mouse.get_pos()):
					sys.exit(0)

				elif pygame.Rect(volume.left, volume.top, volume.width, volume.height).collidepoint(pygame.mouse.get_pos()):
					volume.img = "images/menusprites/volume.png"
					pygame.display.update()
					vol = not vol
					print vol
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit(0)