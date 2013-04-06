
#Frames per second
FPS = 30

#Milliseconds per frame
mSPF = 1000.0/float(FPS)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

DEFAULT_BGCOLOR = 36, 48, 59
LEVEL0_BGCOLOR = 160, 224, 248
LEVEL1_BGCOLOR = 248, 248, 224
LEVEL3_BGCOLOR = 0, 0, 32


#AI constants
NONE        = 0     #doesn't do anything
FLOOR       = 1     #runs on floor
PLATFORM    = 2     #patrols platform
JUMP        = 3     #static jump (randomly)
HOP         = 4     #hop around (randomly)
FLYVERT     = 5     #fly up and down
FLYHORIZ    = 6     #fly left and right
FLYSWOOP    = 7     #fly in a parabola
FLYATTACK   = 8     #(start offscreen) and swoop to player
RPROJ       = 9     #randomly shoot projectiles and follow player
RPROJSTAND  = 10    #randomly stand still and shoot projectiles

PLAYER_LIVES = 3
