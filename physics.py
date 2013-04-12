import eventmanager
import level
import pygame
from constants import DOWN,UP,LEFT,RIGHT
from level import *

class physics(object):
    def __init__(self):
        pass

    #a = entity1, b = entity2
    #offset = amount to subtract from b's bounding rectangle
    def handleCollision(self, a, b):
        #sentinel overlap values
        topOverlap = -500
        botOverlap = 500
        leftOverlap = -500
        rightOverlap = 500
        
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
        #top overlap
        if min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(topOverlap):
            if(topOverlap != -500):
                a.stallY()
                a.rect.top = b.rect.bottom
        #bottom overlap
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == botOverlap:
            if(botOverlap != 500):
                a.stallY()
                a.isJumping = False
                a.rect.bottom = b.rect.top
                #check for teleporter
                if b.teleporter == True and b.teleportDir == DOWN and eventmanager.get().DOWNPRESSED:
                    if a.rect.left > b.rect.left and a.rect.right < b.rect.right:
                        b.teleport()
        #left overlap
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == abs(leftOverlap):
            if(leftOverlap != -500):
                a.stallX()
                a.rect.left = b.rect.right
        #right overlap
        elif min(abs(topOverlap), botOverlap, abs(leftOverlap), rightOverlap) == rightOverlap:
            if(rightOverlap != 500):
                a.stallX()
                a.rect.right = b.rect.left

        b.try_hurt(a)

#Create singleton accessible through physics.get()
__instance = physics()
def get(): return __instance
