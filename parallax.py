"""
    class to add depth to background
    images to use should be wider than the camera width (600px)
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
            self.rect1copy = self.img1.get_rect()
            self.rect1copy.topleft = (x1,y1)
        if img2:
            self.x2 = x2
            self.img2 = StaticAnimation(img2)
            self.rect2 = self.img2.get_rect()
            self.rect2.topleft = (x2,y2)
            #copy of the second image for when img2 is done
            self.x2copy = None
            self.rect2copy = self.img2.get_rect()
            self.rect2.topleft = (x2,y2)

    # x = player.rect.x, y = player.rect.y
    def update(self,x,y):
        if not self.prevDist:
            self.prevDist = x
        else:
            img1Dist = (x-self.prevDist)/10.0
            img2Dist = (x-self.prevDist)/5.0
            #move origs + copies
            if self.rect1:
                self.rect1.x -= img1Dist
            if self.x1copy:
                self.rect1copy.x -= img1Dist
            if self.rect2:
                self.rect2.x -= img2Dist
            if self.x2copy:
                self.rect2copy.x -= img2Dist
            self.prevDist = x

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

        #bg images need to be looped on right side
        if camera.window.right > self.x1 + self.rect2.width and not self.x1copy:
            self.x1copy = camera.window.right
            self.rect1copy.x = self.x1copy
        if camera.window.right > self.x2 + self.rect2.width and not self.x2copy:
            self.x2copy = camera.window.right
            self.rect2copy.x = self.x2copy

        #bg images need to be looped on left side
        if not self.x1copy and camera.window.left < self.x1:
            self.x1copy = camera.window.left - self.rect1.width
            self.rect1copy.x = self.x1copy
        if not self.x2copy and camera.window.left < self.x2:
            self.x2copy = camera.window.left- self.rect2.width
            self.rect2copy.x = self.x2copy

        #camera's left edge has passed the original bg image
        #make the copy image the original
        if camera.window.left > self.x1 + self.rect1.width and self.x1copy:
            self.x1 = self.x1copy
            self.rect1.x = self.x1
            self.x1copy = None
        if camera.window.left > self.x2 + self.rect2.width and self.x2copy:
            self.x2 = self.x2copy
            self.rect2.x = self.x2
            self.x2copy = None

        #camera's right edge has passed the original bg image
        #make the copy image the original
        if camera.window.right < self.x1 and self.x1copy:
            self.x1 = self.x1copy
            self.rect1.x = self.x1
            self.x1copy = None
        if camera.window.right < self.x2 and self.x2copy:
            self.x2 = self.x2copy
            self.rect2.x = self.x2
            self.x2copy = None
