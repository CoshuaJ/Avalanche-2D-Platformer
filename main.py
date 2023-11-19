import pygame
from constants import *
from level import *
from player import *
from menu import *
import copy

'''
Eruption by Josh Costa
Inspired by 'Avalanche' developed by The Game Homepage, found at: https://www.addictinggames.com/action/avalanche
Solo WR: 1443 by me, 21/06/23
'''

# Initialize Pygame
pygame.init()

# display settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eruption")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# game data
is_hard = True
game_state = MENU
try:
    with open("PB.txt", 'r') as file:
        PB_score = int(file.read())
except FileNotFoundError:
    PB_score = 0
last_score = 0
FONT = pygame.font.Font(FONT_STR, 30)
palette = rand_palette()
menu = Menu(screen, palette)
level_type = Leveltype.SOLO
curr_level = None

def set_level(type):
    if type == Leveltype.PRAC:
        return Level(screen, palette, is_hard=False)
    elif type == Leveltype.SOLO:
        return Level(screen, palette)
    elif type == Leveltype.DUO:
        return Level2P(screen, palette)
    elif type == Leveltype.AI:
        return None
    else:
        return None


# main game loop
window_running = True
while window_running:
    # window logic
    for event in pygame.event.get():
        # clicked red X OR pressed Esc
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            window_running = False
            continue
    # record current frame inputs
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()
    # start menu
    if game_state == MENU:
        new_level_type = menu.update(keys, mouse_pos, mouse_btns)
        if new_level_type is None:
            menu.draw()
        else:
            level_type = new_level_type
            curr_level = set_level(level_type)
            game_state = ACTIVE
        # text
        pb_text = FONT.render("PB: " + str(PB_score), False, palette[GROUND])
        last_text = FONT.render("LAST: " + str(last_score), False, palette[GROUND])
        screen.blit(pb_text, (WIDTH-180, 0))
        screen.blit(last_text, (5, 0))
        # if R pressed
        if keys[pygame.K_r]:
            curr_level = set_level(level_type)
            game_state = ACTIVE

    # level logic
    elif game_state == ACTIVE:
        # level status not running
        if not curr_level.running:
            # PB check
            if curr_level.max_score > PB_score:
                PB_score = curr_level.max_score
                # update PB.txt file
                with open("PB.txt", 'w') as file:
                    file.write(str(PB_score))
            last_score = int(curr_level.max_score)
            game_state = MENU
            palette = rand_palette()
            menu = Menu(screen, palette)
            curr_level = None
        # level running
        else:
            # reset key
            if keys[pygame.K_r]:
                curr_level = set_level(level_type)
                game_state = ACTIVE
            curr_level.update()
            curr_level.draw()

    # error screen
    else:
        screen.fill('black')
        print("game_state invalid")
        window_running = False

    # Update the display
    pygame.display.update()
    # caps framerate
    clock.tick(FPS)

# close Pygame
pygame.quit()

