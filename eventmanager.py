import sys
import pygame
from pygame.locals import *

class EventManager:

    def __init__(self):
        self.LEFTPRESSED = False
        self.RIGHTPRESSED = False
        self.UPPRESSED = False
        self.DOWNPRESSED = False
        self.SPACEPRESSED = False
        self.NORMPRESSED = False    #normal attack
        self.SPECPRESSED = False    #special attack

    def handleEvents(self,events):
        """Deal with all the events from pygame. The events have to be passed in since
        pygame wasn't actually initalized in this module"""

        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Exiting....")
                pygame.quit()
                sys.exit(0)

            elif event.type == MOUSEMOTION:     pass
            elif event.type == MOUSEBUTTONDOWN: pass

            elif event.type == KEYDOWN or event.type == KEYUP:
                if   event.key == K_LEFT  : self.LEFTPRESSED  = event.type == KEYDOWN
                elif event.key == K_RIGHT : self.RIGHTPRESSED = event.type == KEYDOWN
                elif event.key == K_UP    : self.UPPRESSED    = event.type == KEYDOWN
                elif event.key == K_DOWN  : self.DOWNPRESSED  = event.type == KEYDOWN
                elif event.key == K_SPACE : self.SPACEPRESSED = event.type == KEYDOWN
                elif event.key == K_SPACE : self.SPACEPRESSED = event.type == KEYDOWN
                elif event.key == K_a     : self.NORMPRESSED = event.type == KEYDOWN
                elif event.key == K_s     : self.SPECPRESSED = event.type == KEYDOWN

#Create singleton accessible through eventmanager.get()
__instance = EventManager()
def get(): return __instance
