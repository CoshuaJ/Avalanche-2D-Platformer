import pygame
from constants import *
from level import *
from player import *
from menu import *

'''
Eruption by Josh Costa
Inspired by 'Avalanche' developed by The Game Homepage, found at: https://www.addictinggames.com/action/avalanche
Hard Mode WR: 953 by Me, 08/03/23
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
with open("PB.txt", 'r') as file:
    PB_score = int(file.read())
last_score = 0
FONT = pygame.font.Font(FONT_STR, 30)
palette = rand_palette()
menu = Menu(screen, palette)
level = None

# main game loop
window_running = True
while window_running:
    # window logic
    for event in pygame.event.get():
        # clicked red X
        if event.type == pygame.QUIT:
            window_running = False
            continue
        # pressed Esc
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            window_running = False
            continue
    # record current frame inputs
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()
    # start menu
    if game_state == MENU:
        level = menu.update(keys, mouse_pos, mouse_btns)
        if level is None:
            menu.draw()
        else:
            game_state = ACTIVE
        # text
        pb_text = FONT.render("PB: " + str(PB_score), False, palette[GROUND])
        last_text = FONT.render("LAST: " + str(last_score), False, palette[GROUND])
        screen.blit(pb_text, (WIDTH-180, 0))
        screen.blit(last_text, (5, 0))

        # if R pressed
        if keys[pygame.K_r]:
            level = Level(screen, palette)
            game_state = ACTIVE

    # level logic
    elif game_state == ACTIVE:
        # level status not running
        if not level.running:
            # PB check
            if level.max_score > PB_score:
                PB_score = level.max_score
                # update PB.txt file
                with open("PB.txt", 'w') as file:
                    file.write(str(PB_score))
            last_score = int(level.max_score)
            game_state = MENU
            palette = rand_palette()
            menu = Menu(screen, palette)
            level = None
        # level running
        else:
            # reset key
            if keys[pygame.K_r]:
                level = Level(screen, palette)
            level.update()
            level.draw()

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

