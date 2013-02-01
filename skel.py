import sys, pygame
pygame.init()

size = width, height = 375, 376

#dfine a color#lame
black = 255, 255, 255

#creates window of size size
screen = pygame.display.set_mode(size)

#load image
logo = pygame.image.load("avengers.jpg")

#make a rectangle for the image
ballrect = logo.get_rect()

#runtime
while 1:

	#events include mouse movements, clicks, keypresses etc
    for event in pygame.event.get():
    	
    	#escape or close
        if event.type == pygame.QUIT: sys.exit()
   
    #draws surface 'screen' onto window
    screen.blit(logo, ballrect)

    #update wimdow
    pygame.display.flip()