"""
    class to add depth to background
    images to use should be wider than the camera width (1000px)

    for now:
            img1 should be the main background (ex: mountains in level 1)
            img2 should be something continuously moving (ex: clouds in level 1)

    TODO:   check for looping left... (code commented out in update)

            dynamic adding .. ex: addLvl( image, scrollType, amount, x,y )

"""

from animation import StaticAnimation
from pygame.sprite import Sprite

from math import floor

from constants import SCREEN_WIDTH

class Parallax(Sprite):

    #x and y are the topleft coords for their corresponding img
    #img is the path of the actual image
    #images are from farthest to closest
    def __init__(self, img1,x1,y1, img2=None,x2=None,y2=None):
        Sprite.__init__(self)
        self.prevDist = None
        self.img1 = None
        self.img2 = None

        #corrector for gaps - there are still gaps though -_-
        self.gapCorrector = 5
        #corrector for loading levels
        self.loadCorrector = 900

        self.totalx = 0
        self.prevx = None
        self.dx = 0

        if img1:
            self.img1 = StaticAnimation(img1)
            self.rect1 = self.img1.get_rect()
            self.rect1.topleft = (x1,y1)
            #copy of the first image for when img1 is done
            self.x1copy = False
            self.rect1copy = self.img1.get_rect()
            self.rect1copy.topleft = (x1,y1)
        if img2:
            self.img2 = StaticAnimation(img2)
            self.rect2 = self.img2.get_rect()
            self.rect2.topleft = (x2,y2)
            #copy of the second image for when img2 is done
            self.x2copy = False
            self.rect2copy = self.img2.get_rect()
            self.rect2.topleft = (x2,y2)

    # x = player.rect.x y = player.rect.y
    def update(self,x,y):
        #init values for starting/loading a level
        if not self.prevx:
            self.prevx = x
            #need to start parallax in the right-ish place when loading a level
            if self.img1:
                self.rect1.x = x - self.loadCorrector
            if self.img2:
                self.rect2.x = x - self.loadCorrector
        else:
            #store partial moves
            self.dx += x - self.prevx

            #calculate move amount
            amount1 = -floor(self.dx/10)

            #move images
            if self.rect1:
                self.rect1.move_ip(amount1,0)
            if self.x1copy:
                self.rect1copy.move_ip(amount1,0)
            if self.rect2:
                self.rect2.move_ip(-1,0)
            if self.x2copy:
                self.rect2copy.move_ip(-1,0)

        #reset?
        self.dx %= 10
        #save current x
        self.prevx = x

        #bg images need to be looped on right side
        if x + SCREEN_WIDTH >= self.rect1.right and not self.x1copy:
            self.x1copy = True
            self.rect1copy.x = x + SCREEN_WIDTH - self.gapCorrector
        if x + SCREEN_WIDTH >=  self.rect2.right and not self.x2copy:
            self.x2copy = True
            self.rect2copy.x = x + SCREEN_WIDTH - self.gapCorrector

        """ assumption is that player won't run backwards..

        #bg images need to be looped on left side
        if not self.x1copy and x - SCREEN_WIDTH <= self.rect1.left:
            self.x1copy = True
            self.rect1copy.x = x - (SCREEN_WIDTH + self.rect1copy.width)
        if not self.x2copy and x - SCREEN_WIDTH <= self.rect2.left:
            self.x2copy = True
            self.rect2copy.x = x - (SCREEN_WIDTH + self.rect1copy.width)
        """

        #player passed the original bg image - going right
        #make the original image's rect the copy's
        if x - SCREEN_WIDTH > self.rect1.right and self.x1copy:
            self.rect1.x = self.rect1copy.x
            self.x1copy = False
        if x - SCREEN_WIDTH > self.rect2.right and self.x2copy:
            self.rect2.x = self.rect2copy.x
            self.x2copy = False

        """ assumption is that player won't run backwards

        #player has passed the original bg image - going left
        #make the original image's rect the copy's
        if x + SCREEN_WIDTH < self.rect1.left and self.x1copy:
            self.rect1.x = self.rect1copy.x
            self.x1copy = False
        if x + SCREEN_WIDTH < self.rect2.left and self.x2copy:
            self.x2 = self.x2copy
            self.rect2.x = self.rect2copy.x
            self.x2copy = False
        """

        #TODO
        #free copy image - ex: unseen on left side, unseen on right



    def draw(self,camera):
        #draw main images
        image1 = self.img1.get_image()
        if image1:
            camera.draw(image1,self.rect1)
        image2 = self.img2.get_image()
        if image2:
            camera.draw(image2,self.rect2)
        #draw copies if needed
        if self.x1copy:
            camera.draw(image1,self.rect1copy)
        if self.x2copy:
            camera.draw(image2,self.rect2copy)


