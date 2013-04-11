#frames per second
FPS = 30

#milliseconds per frame
mSPF = 1000.0/float(FPS)

#screen constants
SCREEN_WIDTH    = 1000
SCREEN_HEIGHT   = 600

#background color constants
DEFAULT_BGCOLOR = 36, 48, 59
LEVEL0_BGCOLOR  = 160, 224, 248
LEVEL1_BGCOLOR  = 248, 248, 224
LEVEL3_BGCOLOR  = 0, 0, 32

#directional constants
DOWN    = 0
UP      = 1
LEFT    = 2
RIGHT   = 3

#teleport constants
TELEPORT    = False     #should main game loop handle teleport?
TELEX       = 0         #x in new level to teleport to 
TELEY       = 0         #y in new level to teleport to 
TELELEVEL   = 0         #level to teleport to
TELEDIR     = DOWN      #move player in current level (ex down a pipe)

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
CUSTOM      = 11    #enemy object is going to define its own ai

#player constants
PLAYER_LIVES = 3
