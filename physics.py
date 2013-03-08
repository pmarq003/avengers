import level
from level import *
import pygame

class physics(object):
    def __init__(self):
        #sentinel overlap values
        topOverlap = -500
        botOverlap = 500
        leftOverlap = -500
        rightOverlap = 500
        
    def handleCollision(self,a,b):
        #If either object isn't solid we don't care
        if not a.solid or not b.solid: return

        #check for the actual overlaps
        #from the perspective of the player
        if(a.rect.top - b.rect.bottom < 0):
            topOverlap = a.rect.top - b.rect.bottom
        if(a.rect.bottom - b.rect.top > 0):
            botOverlap = a.rect.bottom- b.rect.top
        if(a.rect.left - b.rect.right < 0):
            leftOverlap = a.rect.left - b.rect.right
        if(a.rect.right - b.rect.left > 0):
            rightOverlap = a.rect.right - b.rect.left

        #correct only the smallest overlap
        if min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(topOverlap):
            a.stallY()
            a.rect.top = b.rect.bottom
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == botOverlap:
            a.stallY()
            a.isJumping = False
            a.rect.bottom = b.rect.top
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(leftOverlap):
            a.stallX()
            a.rect.left = b.rect.right
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == rightOverlap:
            a.stallX()
            a.rect.right = b.rect.left

        b.try_hurt(a)
        
#Create singleton accessible through physics.get()
__instance = physics()
def get(): return __instance