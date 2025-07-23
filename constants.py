# target frames per second
FPS = 60

# virtual resolution used for scaling the game
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 240
VIRTUAL_TILE = 16

# how much the virtual resolution is scaled up for the actual screen
SCREEN_SCALE = 4

# actual screen resolution in pixels
screen_width = VIRTUAL_WIDTH * SCREEN_SCALE
screen_height = VIRTUAL_HEIGHT * SCREEN_SCALE

# interaction range in pixels
INTERACT_RANGE = VIRTUAL_TILE * 2

# fonts (to be initialized elsewhere)
h1 = None
p = None