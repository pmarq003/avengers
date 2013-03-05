"""
    class to add depth to background
"""

import pygame
from animation import StaticAnimation
from pygame.sprite import Sprite

class Parallax(Sprite):

    #x and y are the topleft coords for their corresponding img
    #img is the path of the actual image
    def __init__(self, img1,x1,y1):
        Sprite.__init__(self)
        self.playerVelX = 0
        self.playerVelY = 0

        if img1:
            self.img1 = StaticAnimation(img1)
            self.rect1 = self.img1.get_rect()
            self.rect1.topleft = (x1,y1)

    # x = player.velX, y = player.velY
    def update(self,x,y):
        if self.rect1:
            self.rect1.x -= x/10

    def draw(self,camera):
        image1 = self.img1.get_image()
        if image1:
            camera.draw(image1,self.rect1)
