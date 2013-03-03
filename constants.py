
#Frames per second
FPS = 30

#Milliseconds per frame
mSPF = 1000.0/float(FPS)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
DEFAULT_BGCOLOR = 36, 48, 59


#AI constants
NONE = 0        #doesn't do anything
FLOOR = 1       #runs on floor
PLATFORM = 2    #patrols platform
JUMP = 3        #static jump (randomly)
HOP = 4         #hop around (randomly)
FLYVERT = 5     #fly up and down
FLYSWOOP = 6    #fly in a parabola

PLAYER_LIVES = 3
