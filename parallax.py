"""
    class to add depth to background
"""

from animation import StaticAnimation
from pygame.sprite import Sprite

class Parallax(Sprite):

    #x and y are the topleft coords for their corresponding img
    #img is the path of the actual image
    #images are from farthest to closest
    def __init__(self, img1,x1,y1, img2=None,x2=None,y2=None):
        Sprite.__init__(self)
        self.prevDist = None
        self.img1 = None
        self.img2 = None

        if img1:
            self.x1 = x1
            self.img1 = StaticAnimation(img1)
            self.rect1 = self.img1.get_rect()
            self.rect1.topleft = (x1,y1)
            #copy of the first image for when img1 is done
            self.x1copy = None
            self.img1copy = None
            self.rect1copy = None
        if img2:
            self.x2 = x2
            self.img2 = StaticAnimation(img2)
            self.rect2 = self.img2.get_rect()
            self.rect2.topleft = (x2,y2)
            #copy of the second image for when img2 is done
            self.x2copy = None
            self.img2copy = None
            self.rect2copy = None

    # x = player.rect.x, y = player.rect.y
    def update(self,x,y):
        if not self.prevDist:
            self.prevDist = x
        else:
            if self.rect1:
                self.rect1.x -= (x-self.prevDist)/10.0
            if self.rect2:
                self.rect2.x -= (x-self.prevDist)/5.0
            self.prevDist = x

    def draw(self,camera):
        image1 = self.img1.get_image()
        if image1:
            camera.draw(image1,self.rect1)
        image2 = self.img2.get_image()
        if image2:
            camera.draw(image2,self.rect2)
        #this is when new bg images need to be drawn
        #handles only playing moving right so far..
        if camera.window.right > self.x1 + (self.rect1.right - self.rect1.left):
            print 'blit new image'
