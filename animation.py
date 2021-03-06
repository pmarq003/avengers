import pygame

class Animation(object):

    def __init__( self, base, num_frames, delay=1 ):
        self.base = base #makes debugging easier
        self.curr_frame = 0
        self.toshow = 0
        self.delay_factor = delay
        self.num_frames = num_frames
        self.frames = []
        self.blink = False
        for i in range(0,num_frames):
            #python's format is cool: "blah{0}-{1}".format(1,2) == "blah1-2"
            self.frames.append( pygame.image.load( base.format(i) ) )

    def update(self):
        self.curr_frame = (self.curr_frame+1) % (self.num_frames * self.delay_factor)
        self.toshow = (int)(self.curr_frame / self.delay_factor)

    def reset(self):
        self.blink = False
        self.curr_frame = 0

    def get_image(self):
        if self.blink == False:
            return self.frames[self.toshow]
        elif not isinstance(self.blink,int):
            self.blink = 0
    
        self.blink += 1

        if (self.blink / 2) % 2:
            return None
        else:
            return self.frames[self.toshow]


    def get_rect(self):
        return self.frames[self.toshow].get_rect()

#Might as well just make a new class instead of extending Animation since this one has a
#completely different implementation. Just gotta make sure they keep the same interface so
#we can use them interchangeably
class StaticAnimation(object):
    
    def __init__( self, base ):
        self.base = base #makes debugging easier
        self.image = pygame.image.load( base )
        self.blink = False

    def update(self):
        pass

    def reset(self):
        pass

    def get_image(self):
        if self.blink == False:
            return self.image
        elif not isinstance(self.blink,int):
            self.blink = 0
    
        self.blink += 1

        if (self.blink / 2) % 2:
            return None
        else:
            return self.image

    def get_rect(self):
        return self.image.get_rect()

