import random
import enum

WIDTH = 600
HEIGHT = 750
FPS = 60
PLAYER_W = 35
PLAYER_H = 55
COUNTDOWN = FPS * 10
FONT_STR = 'retro.ttf'

MENU = 0
ACTIVE = 1

PLAYER = 0
BLOCK = 1
SKY = 2
GROUND = 3
LAVA = 4

class Leveltype(enum.Enum):
    PRAC = 0
    SOLO = 1
    DUO = 2
    AI = 3

# colour palettes
PALETTES = [
    # player,   block,    sky,      ground,   lava
    ['#333f58', '#4a7a96', '#fbbbad', '#292831', '#ee8695'],  # peach/cyan **
    ['#ffffff', '#2f256b', '#CC99FF', '#060608', '#9933FF'],  # purple
    ['#ebf9ff', '#18284a', '#acd6f6', '#070810', '#52a5de'],  # light blue *
    ['#ffffff', '#87286a', '#fe6c90', '#260d34', '#d03791'],  # pink *
    ['#272744', '#8b6d9c', '#D2AFB4', '#000000', '#494d7e'],  # yellow/purple
    ['#281a2d', '#6b2341', '#FF6666', '#0d101b', '#af2747'],  # red *
    ['#40332f', '#95c798', '#fbffe0', '#000000', '#FFCCFF'],  # green/pink *
    ['#0f052d', '#36868f', '#CCFFCC', '#000000', '#5fc75d'],  # green/cyan **
    ['#fabb64', '#fd724e', '#5f2f45', '#f5ddbc', '#a02f40']   # orange *
]


# random colour palette
def rand_palette():
    #return PALETTES[8]
    return PALETTES[random.randint(0, len(PALETTES) - 1)]
